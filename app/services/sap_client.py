from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings


class SAPClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def _get_access_token(self) -> str:
        """
        Stub for OAuth client-credentials flow.
        Replace with a production token request against SAP BTP/XSUAA.
        """
        # TODO: Implement real OAuth token request.
        # Example flow:
        #   POST settings.sap_token_url
        #   auth=(client_id, client_secret) or body-based credentials
        #   grant_type=client_credentials
        #   scope=settings.sap_scope (optional)
        return "DUMMY_ACCESS_TOKEN"

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        token = await self._get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/json"

        url = f"{self.settings.sap_cpi_base_url.rstrip('/')}{path}"

        async with httpx.AsyncClient(
            verify=self.settings.sap_verify_ssl,
            timeout=self.settings.sap_timeout_seconds,
        ) as client:
            response = await client.request(method, url, headers=headers, **kwargs)

        # TODO: add retry, richer error handling, OData normalization.
        if response.status_code >= 400:
            raise RuntimeError(
                f"SAP API call failed: {response.status_code} {response.text[:500]}"
            )

        if "application/json" in response.headers.get("content-type", ""):
            return response.json()

        return {"raw_text": response.text}

    async def list_packages(self, name_contains: str | None = None, package_id: str | None = None) -> dict[str, Any]:
        """
        Stub for listing integration packages.
        """
        # TODO: replace with actual OData query logic and pagination.
        sample = {
            "d": {
                "results": [
                    {
                        "Id": "PKG_ORDER_MGMT",
                        "Name": "Order Management",
                        "ShortText": "Order-related integrations",
                    },
                    {
                        "Id": "PKG_FINANCE",
                        "Name": "Finance Integrations",
                        "ShortText": "Finance interfaces",
                    },
                ]
            }
        }

        results = sample["d"]["results"]

        if name_contains:
            results = [r for r in results if name_contains.lower()
                       in r["Name"].lower()]
        if package_id:
            results = [r for r in results if r["Id"] == package_id]

        return {"items": results, "count": len(results)}

    async def list_iflows(
        self,
        package_id: str | None = None,
        iflow_name_contains: str | None = None,
        iflow_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Stub for listing iFlows.
        """
        # TODO: replace with actual artifact query to SAP.
        sample = [
            {
                "Id": "IR20_IF02_Email_Alert_Notifications_For_SAP_CPI_Tenant",
                "Name": "Email Alert Notifications for SAP CPI Tenant",
                "PackageId": "PKG_ORDER_MGMT",
                "Version": "1.0.3",
                "Deployed": True,
            },
            {
                "Id": "IFLOW_SFTP_TO_ERP",
                "Name": "SFTP to ERP Order Import",
                "PackageId": "PKG_FINANCE",
                "Version": "2.1.0",
                "Deployed": True,
            },
        ]

        results = sample
        if package_id:
            results = [x for x in results if x["PackageId"] == package_id]
        if iflow_name_contains:
            results = [x for x in results if iflow_name_contains.lower()
                       in x["Name"].lower()]
        if iflow_id:
            results = [x for x in results if x["Id"] == iflow_id]

        return {"items": results, "count": len(results)}

    async def get_iflow_content(self, iflow_id: str) -> dict[str, Any]:
        """
        Stub for downloading/parsing the design-time artifact.
        """
        # TODO: replace with actual download/export call to SAP.
        return {
            "iflow_id": iflow_id,
            "name": "Email Alert Notifications for SAP CPI Tenant",
            "content_type": "application/zip",
            "raw_content": b"PK\x03\x04...dummy zip bytes...",
            "metadata": {
                "sender_adapter": "Timer",
                "receiver_adapter": "Mail",
                "authentication": "User Credential",
            },
        }
