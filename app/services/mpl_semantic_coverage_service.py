from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.services.sap_client import SAPClient


@dataclass
class MPLFailureSignal:
    message_guid: str
    iflow_id: str
    iflow_name: str
    status: str
    error_text: str
    normalized_code: str
    taxonomy: str
    timestamp: str
    sender: str
    receiver: str


class MPLSemanticCoverageService:
    """
    Enriches tenant-wide knowledge generation with runtime evidence from MPL.

    The goal is not only to infer likely issue families from design-time artifacts,
    but also to ground KEDB and Runbook generation in real failure signatures
    observed in Message Processing Logs.
    """

    def __init__(self, sap_client: SAPClient, local_mpl_dir: str | None = None) -> None:
        self.sap_client = sap_client
        self.local_mpl_dir = Path(local_mpl_dir) if local_mpl_dir else None

    async def collect_failure_signals(
        self,
        *,
        hours_back: int = 168,
        limit: int = 250,
        status: str = "FAILED",
        local_json_dir: str | None = None,
    ) -> list[MPLFailureSignal]:
        """
        Collect failed-message runtime evidence from live MPL API and/or local JSON corpora.
        """
        signals: list[MPLFailureSignal] = []

        live_error: str | None = None
        try:
            logs = await self.sap_client.list_message_processing_logs(
                status=status,
                hours_back=hours_back,
                top=limit,
            )
            for item in logs.get("items", []):
                error_text = self._clean_error_text(self._extract_best_error_text(item))
                message_guid = str(item.get("MessageGuid") or item.get("Id") or "")
                if message_guid and self._needs_detailed_error(error_text):
                    detail_text = await self._safe_get_error_information(message_guid)
                    if detail_text:
                        error_text = detail_text

                signals.append(
                    MPLFailureSignal(
                        message_guid=message_guid or "UNKNOWN_MESSAGE_GUID",
                        iflow_id=str(item.get("IntegrationFlowName") or item.get("IntegrationArtifact") or "UNKNOWN_IFLOW"),
                        iflow_name=str(item.get("IntegrationFlowName") or item.get("IntegrationArtifact") or "UNKNOWN_IFLOW"),
                        status=str(item.get("Status") or status),
                        error_text=error_text or "Error details are missing in MPL.",
                        normalized_code=self._normalized_code_from_error_text(error_text),
                        taxonomy=self._taxonomy_from_error_text(error_text),
                        timestamp=str(item.get("LogStart") or item.get("LogEnd") or self._now_iso()),
                        sender=str(item.get("Sender") or "Unknown sender"),
                        receiver=str(item.get("Receiver") or "Unknown receiver"),
                    )
                )
        except Exception as exc:  # pragma: no cover - fallback friendly path
            live_error = str(exc)

        local_dir = Path(local_json_dir) if local_json_dir else self.local_mpl_dir
        if local_dir and local_dir.exists():
            signals.extend(self._load_local_json_signals(local_dir=local_dir, limit=limit))

        if not signals and live_error:
            # Keep one synthetic signal so downstream generation still exposes
            # that MPL coverage was requested but unavailable.
            signals.append(
                MPLFailureSignal(
                    message_guid="MPL-COVERAGE-NOT-AVAILABLE",
                    iflow_id="MULTI_INTERFACE",
                    iflow_name="MPL Coverage Not Available",
                    status=status,
                    error_text=f"MPL collection failed: {live_error}",
                    normalized_code="MPL_OBSERVABILITY_ERROR_DETAILS_MISSING",
                    taxonomy="CPI | OBSERVABILITY | ERROR_DETAILS_MISSING | MPL",
                    timestamp=self._now_iso(),
                    sender="Unknown sender",
                    receiver="Unknown receiver",
                )
            )

        return signals[:limit]

    def summarize_signals(self, signals: list[MPLFailureSignal]) -> dict[str, Any]:
        summary: dict[str, dict[str, Any]] = {}
        for signal in signals:
            bucket = summary.setdefault(
                signal.normalized_code,
                {
                    "count": 0,
                    "taxonomy": signal.taxonomy,
                    "example_errors": [],
                    "example_message_guids": [],
                    "iflow_ids": set(),
                    "last_seen": signal.timestamp,
                },
            )
            bucket["count"] += 1
            if len(bucket["example_errors"]) < 3 and signal.error_text not in bucket["example_errors"]:
                bucket["example_errors"].append(signal.error_text)
            if len(bucket["example_message_guids"]) < 5 and signal.message_guid not in bucket["example_message_guids"]:
                bucket["example_message_guids"].append(signal.message_guid)
            cast_iflows = bucket["iflow_ids"]
            cast_iflows.add(signal.iflow_id)
            if signal.timestamp > bucket["last_seen"]:
                bucket["last_seen"] = signal.timestamp

        normalized: dict[str, Any] = {}
        for code, value in summary.items():
            normalized[code] = {
                "count": value["count"],
                "taxonomy": value["taxonomy"],
                "example_errors": value["example_errors"],
                "example_message_guids": value["example_message_guids"],
                "iflow_ids": sorted(value["iflow_ids"]),
                "last_seen": value["last_seen"],
            }
        return normalized

    def _load_local_json_signals(self, local_dir: Path, limit: int) -> list[MPLFailureSignal]:
        signals: list[MPLFailureSignal] = []
        for path in sorted(local_dir.rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            records = self._flatten_records(data)
            for item in records:
                if str(item.get("Status") or item.get("status") or "FAILED").upper() != "FAILED":
                    continue
                error_text = self._clean_error_text(
                    str(item.get("ErrorMessage") or item.get("localizedText") or item.get("error_text") or item.get("ErrorDetails") or "")
                )
                message_guid = str(item.get("MessageGuid") or item.get("messageID") or item.get("message_guid") or path.stem)
                iflow_name = str(item.get("IntegrationFlowName") or item.get("interface") or item.get("iflow_id") or "UNKNOWN_IFLOW")
                signals.append(
                    MPLFailureSignal(
                        message_guid=message_guid,
                        iflow_id=iflow_name,
                        iflow_name=iflow_name,
                        status="FAILED",
                        error_text=error_text or "Error details are missing in local MPL corpus.",
                        normalized_code=self._normalized_code_from_error_text(error_text),
                        taxonomy=self._taxonomy_from_error_text(error_text),
                        timestamp=str(item.get("LogStart") or item.get("timeStamp") or self._now_iso()),
                        sender=str(item.get("Sender") or item.get("sender") or "Unknown sender"),
                        receiver=str(item.get("Receiver") or item.get("receiver") or "Unknown receiver"),
                    )
                )
                if len(signals) >= limit:
                    return signals
        return signals

    def _flatten_records(self, data: Any) -> list[dict[str, Any]]:
        if isinstance(data, list):
            return [x for x in data if isinstance(x, dict)]
        if isinstance(data, dict):
            if isinstance(data.get("d"), dict) and isinstance(data["d"].get("results"), list):
                return [x for x in data["d"]["results"] if isinstance(x, dict)]
            if isinstance(data.get("value"), list):
                return [x for x in data["value"] if isinstance(x, dict)]
            for key in ("records", "MessageErrors", "MessageProcessingLogs", "items"):
                if isinstance(data.get(key), list):
                    return [x for x in data[key] if isinstance(x, dict)]
            return [data]
        return []

    async def _safe_get_error_information(self, message_guid: str) -> str:
        try:
            return await self.sap_client.get_error_information_text(message_guid=message_guid)
        except Exception:
            return ""


    def _clean_error_text(self, error_text: str) -> str:
        text = (error_text or "").strip()
        if not text:
            return ""
        text = re.sub(r"^[A-Za-z0-9_.:$]+(?:Exception|Error):\s*", "", text)
        text = re.sub(r"\n?The MPL ID for the failed message is\s*:\s*[A-Za-z0-9_\-]+", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n{2,}", "\n", text).strip(" .\n")
        return text

    def _extract_best_error_text(self, item: dict[str, Any]) -> str:
        for key in (
            "ErrorMessage",
            "errorMessage",
            "LocalizedErrorText",
            "ExceptionMessage",
            "CustomStatus",
        ):
            value = item.get(key)
            if value is not None and str(value).strip():
                return str(value)
        return ""

    def _needs_detailed_error(self, error_text: str) -> bool:
        cleaned = (error_text or "").strip().lower()
        return cleaned in {"", "n/a", "unknown", "error details are missing in mpl."}

    def _normalized_code_from_error_text(self, error_text: str) -> str:
        text = (error_text or "").lower()
        if "401" in text or "unauthorized" in text:
            return "HTTP_AUTHENTICATION_UNAUTHORIZED_401"
        if "500" in text or "internal server error" in text:
            return "DOWNSTREAM_SERVER_INTERNAL_ERROR_500"
        if "503" in text or "service unavailable" in text:
            return "DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503"
        if "smtp" in text or "mail" in text:
            return "MAIL_SMTP_CONFIG_OR_AUTH_FAILURE"
        if "queue has not enough values" in text or "type conversion" in text or "cannot cast" in text:
            return "MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED"
        if "mandatory" in text or "missing" in text:
            return "MAPPING_SOURCE_MANDATORY_VALUE_MISSING"
        if "token" in text and ("expired" in text or "session" in text):
            return "CLOUD_AUTH_SESSION_EXPIRED"
        if not text.strip():
            return "MPL_OBSERVABILITY_ERROR_DETAILS_MISSING"
        normalized = re.sub(r"[^a-z0-9]+", "_", text).strip("_").upper()
        normalized = re.sub(r"_+", "_", normalized)
        return normalized[:72] or "MPL_OBSERVABILITY_ERROR_DETAILS_MISSING"

    def _taxonomy_from_error_text(self, error_text: str) -> str:
        code = self._normalized_code_from_error_text(error_text)
        mapping = {
            "HTTP_AUTHENTICATION_UNAUTHORIZED_401": "HTTP | AUTHENTICATION | UNAUTHORIZED | 401",
            "DOWNSTREAM_SERVER_INTERNAL_ERROR_500": "HTTP | DOWNSTREAM | INTERNAL_SERVER_ERROR | 500",
            "DOWNSTREAM_AVAILABILITY_SERVICE_UNAVAILABLE_503": "HTTP | AVAILABILITY | SERVICE_UNAVAILABLE | 503",
            "MAIL_SMTP_CONFIG_OR_AUTH_FAILURE": "MAIL | SMTP | CONFIG_OR_AUTH_FAILURE | DELIVERY",
            "MAPPING_TRANSFORMATION_TYPE_CONVERSION_FAILED": "MAPPING | TRANSFORMATION | TYPE_CONVERSION_FAILED | DATA",
            "MAPPING_SOURCE_MANDATORY_VALUE_MISSING": "MAPPING | DATA_QUALITY | MANDATORY_VALUE_MISSING | SOURCE",
            "CLOUD_AUTH_SESSION_EXPIRED": "CLOUD | AUTHENTICATION | SESSION_EXPIRED | TOKEN",
            "MPL_OBSERVABILITY_ERROR_DETAILS_MISSING": "CPI | OBSERVABILITY | ERROR_DETAILS_MISSING | MPL",
        }
        return mapping.get(code, " | ".join([x for x in code.split("_") if x]))

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
