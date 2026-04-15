from __future__ import annotations


class ScoringService:
    def __init__(self, max_score: int = 100) -> None:
        self.max_score = max_score

    def score_iflow(self, iflow_id: str, analysis: dict) -> dict:
        issues: list[dict] = []
        score = self.max_score

        authentication = analysis.get("authentication", [])
        protocols = analysis.get("protocols", [])

        if not authentication or "Unknown" in authentication:
            issues.append(
                {
                    "category": "Authentication Clarity",
                    "severity": "medium",
                    "points_deducted": 8,
                    "message": "Authentication method is missing or not clearly identifiable.",
                    "recommendation": "Document and validate the credential type and security material used.",
                }
            )
            score -= 8

        if "SMTP" in protocols:
            issues.append(
                {
                    "category": "Operational Dependency Visibility",
                    "severity": "low",
                    "points_deducted": 3,
                    "message": "Mail-based notifications create external operational dependencies.",
                    "recommendation": "Confirm mail channel ownership, alert routing, and fallback handling.",
                }
            )
            score -= 3

        summary = (
            "Stub quality result. Replace with the 15-category enterprise anti-pattern engine "
            "in the next iteration."
        )

        return {
            "iflow_id": iflow_id,
            "score": max(score, 0),
            "max_score": self.max_score,
            "issues": issues,
            "summary": summary,
        }
