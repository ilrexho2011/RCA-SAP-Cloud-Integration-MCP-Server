from __future__ import annotations

from typing import Any


class IFlowParser:
    def parse(self, artifact_payload: dict[str, Any]) -> dict[str, Any]:
        """
        Stub parser. In production this should:
        - unzip the design-time artifact
        - inspect integration flow model/config files
        - detect adapters, endpoints, scripts, mappings, security materials
        """
        metadata = artifact_payload.get("metadata", {})
        return {
            "summary": (
                "This iFlow appears to trigger on a schedule and send alert notifications "
                "via Mail adapter."
            ),
            "sender_systems": ["Internal CPI Timer"],
            "receiver_systems": ["Mail Server / Notification Target"],
            "protocols": ["Timer", "SMTP"],
            "authentication": [metadata.get("authentication", "Unknown")],
            "dependencies": ["Mail adapter", "User credential"],
            "raw_metadata": metadata,
        }
