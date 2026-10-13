from __future__ import annotations

from typing import Any


class ScoringService:
    """Enterprise scoring engine for SAP CPI iFlow analysis results.

    This service supports both:
    - zip_based analysis: configuration-level evidence extracted from the iFlow package
    - metadata_only analysis: tenant metadata without deep configuration visibility

    The output is designed to be useful for:
    - MCP documentation generation
    - audit-style reporting
    - machine-readable downstream quality gates
    """

    ZIP_BASED_MODE = "zip_based"
    METADATA_ONLY_MODE = "metadata_only"
    UNKNOWN_MODE = "unknown"

    UNKNOWN_TOKENS = {
        "unknown",
        "n/a",
        "not available",
        "not exposed",
        "not found",
        "undetermined",
        "none",
        "null",
        "",
    }

    # Weighted scoring matrices on a raw 100-point basis.
    MATRIX_BY_MODE = {
        ZIP_BASED_MODE: [
            {"key": "analysis_mode_integrity", "label": "Analysis Mode Integrity", "weight": 6},
            {"key": "authentication_clarity", "label": "Authentication Clarity", "weight": 16},
            {"key": "protocol_clarity", "label": "Protocol Clarity", "weight": 14},
            {"key": "sender_traceability", "label": "Sender Traceability", "weight": 10},
            {"key": "receiver_traceability", "label": "Receiver Traceability", "weight": 10},
            {"key": "package_resolution", "label": "Package Resolution", "weight": 8},
            {"key": "version_resolution", "label": "Version Resolution", "weight": 8},
            {"key": "summary_quality", "label": "Summary Quality", "weight": 8},
            {"key": "operational_dependency_visibility", "label": "Operational Dependency Visibility", "weight": 8},
            {"key": "evidence_consistency", "label": "Evidence Consistency", "weight": 12},
        ],
        METADATA_ONLY_MODE: [
            {"key": "analysis_mode_integrity", "label": "Analysis Mode Integrity", "weight": 10},
            {"key": "authentication_visibility", "label": "Authentication Visibility", "weight": 10},
            {"key": "protocol_visibility", "label": "Protocol Visibility", "weight": 10},
            {"key": "sender_visibility", "label": "Sender Visibility", "weight": 8},
            {"key": "receiver_visibility", "label": "Receiver Visibility", "weight": 8},
            {"key": "package_resolution", "label": "Package Resolution", "weight": 14},
            {"key": "version_resolution", "label": "Version Resolution", "weight": 14},
            {"key": "summary_quality", "label": "Summary Quality", "weight": 12},
            {"key": "operational_dependency_visibility", "label": "Operational Dependency Visibility", "weight": 4},
            {"key": "metadata_observability", "label": "Metadata Observability", "weight": 10},
        ],
    }

    def __init__(self, max_score: int = 100) -> None:
        self.max_score = max_score

    def score_iflow(self, iflow_id: str, analysis: dict[str, Any]) -> dict[str, Any]:
        context = self._collect_context(analysis)
        issues: list[dict[str, Any]] = []

        analysis_mode = context["analysis_mode"]
        matrix_definition = self.MATRIX_BY_MODE.get(
            analysis_mode, self.MATRIX_BY_MODE[self.METADATA_ONLY_MODE]
        )

        weighted_scoring_matrix: list[dict[str, Any]] = []
        raw_score = 0.0

        for item in matrix_definition:
            row = self._evaluate_dimension(item=item, context=context, issues=issues)
            weighted_scoring_matrix.append(row)
            raw_score += row["points_awarded"]

        raw_score = max(0.0, min(100.0, round(raw_score, 2)))
        final_score = int(round((raw_score / 100.0) * self.max_score))

        evidence_coverage = self._build_evidence_coverage(context)
        confidence_score, confidence_level = self._build_confidence(
            analysis_mode=analysis_mode,
            evidence_coverage_percentage=evidence_coverage["percentage"],
        )
        anti_pattern_categories = self._build_anti_pattern_categories(issues)
        audit_output = self._build_audit_output(
            iflow_id=iflow_id,
            context=context,
            final_score=final_score,
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            evidence_coverage=evidence_coverage,
            anti_pattern_categories=anti_pattern_categories,
        )
        summary = self._build_summary(
            iflow_id=iflow_id,
            context=context,
            final_score=final_score,
            confidence_level=confidence_level,
            evidence_coverage=evidence_coverage,
            issues=issues,
        )

        return {
            "iflow_id": iflow_id,
            "analysis_mode": analysis_mode,
            "scoring_profile": self._get_scoring_profile(analysis_mode),
            "score": final_score,
            "max_score": self.max_score,
            "raw_score_100": raw_score,
            "confidence_level": confidence_level,
            "confidence_score": confidence_score,
            "evidence_coverage": evidence_coverage,
            "anti_pattern_categories": anti_pattern_categories,
            "issues": issues,
            "weighted_scoring_matrix": weighted_scoring_matrix,
            "audit_output": audit_output,
            "summary": summary,
        }

    def _collect_context(self, analysis: dict[str, Any]) -> dict[str, Any]:
        return {
            "analysis_mode": self._detect_analysis_mode(analysis),
            "mode_was_explicit": self._mode_was_explicit(analysis),
            "authentication": self._normalize_list(analysis.get("authentication")),
            "protocols": self._normalize_list(analysis.get("protocols")),
            "sender_systems": self._normalize_list(analysis.get("sender_systems")),
            "receiver_systems": self._normalize_list(analysis.get("receiver_systems")),
            "package_name": self._first_non_empty(
                analysis.get("package_name"),
                analysis.get("package"),
                analysis.get("package_id"),
            ),
            "resolved_version": self._first_non_empty(
                analysis.get("resolved_version"),
                analysis.get("version"),
                analysis.get("artifact_version"),
            ),
            "summary": str(analysis.get("summary", "")).strip(),
            "analysis": analysis,
        }

    def _evaluate_dimension(
        self,
        item: dict[str, Any],
        context: dict[str, Any],
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        key = item["key"]
        weight = float(item["weight"])
        label = str(item["label"])

        handler = getattr(self, f"_score_{key}")
        result = handler(context, weight, issues)

        points_awarded = round(max(0.0, min(weight, result["points_awarded"])), 2)
        points_deducted = round(weight - points_awarded, 2)

        return {
            "dimension": key,
            "label": label,
            "weight": weight,
            "max_points": weight,
            "points_awarded": points_awarded,
            "points_deducted": points_deducted,
            "status": result["status"],
            "evidence_field": result["evidence_field"],
            "rationale": result["rationale"],
        }

    def _score_analysis_mode_integrity(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        analysis_mode = context["analysis_mode"]
        explicit = context["mode_was_explicit"]

        if analysis_mode in {self.ZIP_BASED_MODE, self.METADATA_ONLY_MODE} and explicit:
            return self._dimension_result(
                weight,
                "strong",
                "analysis_mode",
                "Analysis mode was explicitly provided by the parser output.",
            )

        if analysis_mode in {self.ZIP_BASED_MODE, self.METADATA_ONLY_MODE}:
            issues.append(
                self._issue(
                    anti_pattern_code="MODE_DETECTION_FALLBACK",
                    category="Analysis Mode Detection",
                    severity="low",
                    issue_type="documentation_gap",
                    points_deducted=round(weight * 0.4, 2),
                    message="Analysis mode was inferred indirectly instead of being emitted explicitly.",
                    recommendation="Emit analysis_mode explicitly from the parser to improve scoring reliability.",
                )
            )
            return self._dimension_result(
                round(weight * 0.6, 2),
                "moderate",
                "analysis_mode",
                "Analysis mode was inferred from the summary or fallback fields.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="MODE_DETECTION_UNCERTAIN",
                category="Analysis Mode Detection",
                severity="medium",
                issue_type="documentation_gap",
                points_deducted=round(weight * 0.7, 2),
                message="Analysis mode could not be detected with confidence.",
                recommendation="Return analysis_mode explicitly as zip_based or metadata_only from the parser output.",
            )
        )
        return self._dimension_result(
            round(weight * 0.3, 2),
            "weak",
            "analysis_mode",
            "Analysis mode is uncertain, so fallback rules were used.",
        )

    def _score_authentication_clarity(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        authentication = context["authentication"]

        if self._has_confirmed_values(authentication):
            return self._dimension_result(
                weight,
                "strong",
                "authentication",
                f"Authentication evidence detected: {', '.join(authentication)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="AUTHENTICATION_OPACITY",
                category="Authentication Clarity",
                severity="medium",
                issue_type="design_risk",
                points_deducted=weight,
                message="Authentication method is missing or not clearly identifiable in zip_based analysis.",
                recommendation="Inspect adapter security settings and document the credential type and security material explicitly.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "authentication",
            "No reliable authentication evidence was detected in the extracted package content.",
        )

    def _score_authentication_visibility(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        authentication = context["authentication"]

        if self._has_confirmed_values(authentication):
            return self._dimension_result(
                weight,
                "strong",
                "authentication",
                f"Authentication metadata is available: {', '.join(authentication)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="AUTHENTICATION_VISIBILITY_LIMITATION",
                category="Authentication Visibility",
                severity="low",
                issue_type="visibility_limitation",
                points_deducted=round(weight * 0.5, 2),
                message="Authentication could not be confirmed from metadata_only analysis.",
                recommendation="Treat this as limited observability. Use zip_based analysis for configuration-level authentication validation.",
            )
        )
        return self._dimension_result(
            round(weight * 0.5, 2),
            "limited",
            "authentication",
            "Authentication is not exposed by metadata and therefore only partially assessable.",
        )

    def _score_protocol_clarity(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        protocols = context["protocols"]

        if self._has_confirmed_values(protocols):
            return self._dimension_result(
                weight,
                "strong",
                "protocols",
                f"Protocol evidence detected: {', '.join(protocols)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="PROTOCOL_OPACITY",
                category="Protocol Clarity",
                severity="medium",
                issue_type="design_risk",
                points_deducted=weight,
                message="Communication protocol could not be identified in zip_based analysis.",
                recommendation="Inspect sender and receiver adapter configuration and surface protocol details in documentation output.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "protocols",
            "No reliable protocol evidence was detected.",
        )

    def _score_protocol_visibility(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        protocols = context["protocols"]

        if self._has_confirmed_values(protocols):
            return self._dimension_result(
                weight,
                "strong",
                "protocols",
                f"Protocol metadata is available: {', '.join(protocols)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="PROTOCOL_VISIBILITY_LIMITATION",
                category="Protocol Visibility",
                severity="low",
                issue_type="visibility_limitation",
                points_deducted=round(weight * 0.5, 2),
                message="Protocol information could not be derived confidently from metadata_only analysis.",
                recommendation="Use zip_based analysis when protocol-level certainty is required in audit output.",
            )
        )
        return self._dimension_result(
            round(weight * 0.5, 2),
            "limited",
            "protocols",
            "Protocols are partially assessable from metadata and may be hidden by tenant exposure limits.",
        )

    def _score_sender_traceability(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        sender_systems = context["sender_systems"]

        if self._has_confirmed_values(sender_systems):
            return self._dimension_result(
                weight,
                "strong",
                "sender_systems",
                f"Sender evidence detected: {', '.join(sender_systems)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="SENDER_TRACEABILITY_GAP",
                category="Sender Traceability",
                severity="medium",
                issue_type="design_risk",
                points_deducted=weight,
                message="Sender system details are missing or unclear in zip_based analysis.",
                recommendation="Verify sender adapter naming, participant modeling, and endpoint ownership documentation.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "sender_systems",
            "Sender systems are not reliably traceable from the available package evidence.",
        )

    def _score_sender_visibility(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        sender_systems = context["sender_systems"]

        if self._has_confirmed_values(sender_systems):
            return self._dimension_result(
                weight,
                "strong",
                "sender_systems",
                f"Sender metadata is available: {', '.join(sender_systems)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="SENDER_VISIBILITY_LIMITATION",
                category="Sender Visibility",
                severity="low",
                issue_type="visibility_limitation",
                points_deducted=round(weight * 0.5, 2),
                message="Sender details were not exposed by metadata_only analysis.",
                recommendation="Do not treat this as a hard design issue. Use zip_based analysis when sender-level evidence is required.",
            )
        )
        return self._dimension_result(
            round(weight * 0.5, 2),
            "limited",
            "sender_systems",
            "Sender visibility is partially constrained by tenant metadata exposure.",
        )

    def _score_receiver_traceability(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        receiver_systems = context["receiver_systems"]

        if self._has_confirmed_values(receiver_systems):
            return self._dimension_result(
                weight,
                "strong",
                "receiver_systems",
                f"Receiver evidence detected: {', '.join(receiver_systems)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="RECEIVER_TRACEABILITY_GAP",
                category="Receiver Traceability",
                severity="medium",
                issue_type="design_risk",
                points_deducted=weight,
                message="Receiver system details are missing or unclear in zip_based analysis.",
                recommendation="Verify receiver adapter naming, endpoint traceability, and target-system ownership.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "receiver_systems",
            "Receiver systems are not reliably traceable from the available package evidence.",
        )

    def _score_receiver_visibility(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        receiver_systems = context["receiver_systems"]

        if self._has_confirmed_values(receiver_systems):
            return self._dimension_result(
                weight,
                "strong",
                "receiver_systems",
                f"Receiver metadata is available: {', '.join(receiver_systems)}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="RECEIVER_VISIBILITY_LIMITATION",
                category="Receiver Visibility",
                severity="low",
                issue_type="visibility_limitation",
                points_deducted=round(weight * 0.5, 2),
                message="Receiver details were not exposed by metadata_only analysis.",
                recommendation="Do not treat this as a hard design issue. Use zip_based analysis when receiver-level evidence is required.",
            )
        )
        return self._dimension_result(
            round(weight * 0.5, 2),
            "limited",
            "receiver_systems",
            "Receiver visibility is partially constrained by tenant metadata exposure.",
        )

    def _score_package_resolution(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        package_name = context["package_name"]

        if package_name and not self._is_unknown_value(package_name):
            return self._dimension_result(
                weight,
                "strong",
                "package_name",
                f"Package was resolved successfully: {package_name}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="PACKAGE_RESOLUTION_GAP",
                category="Package Resolution",
                severity="medium",
                issue_type="documentation_gap",
                points_deducted=weight,
                message="The package name could not be resolved from the analysis payload.",
                recommendation="Expose package_name in parser output so documentation and audit reports remain traceable to the source artifact.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "package_name",
            "Package information is missing or not usable.",
        )

    def _score_version_resolution(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        resolved_version = context["resolved_version"]

        if resolved_version and not self._is_unknown_value(resolved_version):
            return self._dimension_result(
                weight,
                "strong",
                "resolved_version",
                f"Resolved version is available: {resolved_version}.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="VERSION_RESOLUTION_GAP",
                category="Version Resolution",
                severity="medium",
                issue_type="documentation_gap",
                points_deducted=weight,
                message="Resolved version could not be determined from the analysis payload.",
                recommendation="Expose resolved_version explicitly so audit output can reference an exact artifact version.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "resolved_version",
            "Resolved version is missing or ambiguous.",
        )

    def _score_summary_quality(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        summary = context["summary"]
        length = len(summary)

        if length >= 180:
            return self._dimension_result(
                weight,
                "strong",
                "summary",
                "Summary is sufficiently detailed for documentation output.",
            )

        if length >= 80:
            issues.append(
                self._issue(
                    anti_pattern_code="SUMMARY_TOO_BRIEF",
                    category="Summary Quality",
                    severity="low",
                    issue_type="documentation_gap",
                    points_deducted=round(weight * 0.4, 2),
                    message="Summary exists but remains brief for enterprise documentation output.",
                    recommendation="Enrich the summary with the integration purpose, systems, protocols, and authentication posture.",
                )
            )
            return self._dimension_result(
                round(weight * 0.6, 2),
                "moderate",
                "summary",
                "Summary is usable but still too short for high-quality audit narratives.",
            )

        if length > 0:
            issues.append(
                self._issue(
                    anti_pattern_code="SUMMARY_WEAK",
                    category="Summary Quality",
                    severity="medium",
                    issue_type="documentation_gap",
                    points_deducted=round(weight * 0.75, 2),
                    message="Summary is too short to support enterprise documentation output reliably.",
                    recommendation="Generate a richer parser summary that explains purpose, source, target, protocol, and security posture.",
                )
            )
            return self._dimension_result(
                round(weight * 0.25, 2),
                "weak",
                "summary",
                "Summary is present but materially under-detailed.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="SUMMARY_MISSING",
                category="Summary Quality",
                severity="medium",
                issue_type="documentation_gap",
                points_deducted=weight,
                message="Summary is missing from the analysis payload.",
                recommendation="Return a parser-generated summary to support MCP documentation and audit report generation.",
            )
        )
        return self._dimension_result(
            0.0,
            "weak",
            "summary",
            "No summary was provided.",
        )

    def _score_operational_dependency_visibility(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        protocols = context["protocols"]

        if "SMTP" not in protocols:
            return self._dimension_result(
                weight,
                "strong",
                "protocols",
                "No explicit mail-based operational dependency was detected.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="MAIL_DEPENDENCY",
                category="Operational Dependency Visibility",
                severity="low",
                issue_type="operational_risk",
                points_deducted=round(weight * 0.5, 2),
                message="Mail-based notifications create an external operational dependency.",
                recommendation="Confirm mailbox ownership, alert routing, retry strategy, and fallback handling for SMTP-based notifications.",
            )
        )
        return self._dimension_result(
            round(weight * 0.5, 2),
            "moderate",
            "protocols",
            "SMTP dependency detected. This does not invalidate the design, but it should be documented operationally.",
        )

    def _score_evidence_consistency(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        evidence_fields = [
            context["authentication"],
            context["protocols"],
            context["sender_systems"],
            context["receiver_systems"],
            [context["package_name"]] if context["package_name"] else [],
            [context["resolved_version"]] if context["resolved_version"] else [],
        ]
        confirmed_count = sum(1 for field in evidence_fields if self._has_confirmed_values(field))
        ratio = confirmed_count / len(evidence_fields)

        if ratio >= 0.84:
            return self._dimension_result(
                weight,
                "strong",
                "analysis_payload",
                "Evidence set is internally consistent across the key analysis dimensions.",
            )

        if ratio >= 0.5:
            issues.append(
                self._issue(
                    anti_pattern_code="EVIDENCE_PARTIAL_CONSISTENCY",
                    category="Evidence Consistency",
                    severity="low",
                    issue_type="documentation_gap",
                    points_deducted=round(weight * 0.4, 2),
                    message="Evidence is partially consistent, but some dimensions remain weak or missing.",
                    recommendation="Strengthen parser extraction so authentication, protocols, endpoints, package, and version are emitted consistently.",
                )
            )
            return self._dimension_result(
                round(weight * 0.6, 2),
                "moderate",
                "analysis_payload",
                "Evidence is usable but not uniformly strong across all key dimensions.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="EVIDENCE_INCONSISTENCY",
                category="Evidence Consistency",
                severity="medium",
                issue_type="documentation_gap",
                points_deducted=round(weight * 0.75, 2),
                message="Evidence quality is inconsistent across the key analysis dimensions.",
                recommendation="Improve extraction coverage so the documentation pipeline does not rely on sparse or mixed-quality evidence.",
            )
        )
        return self._dimension_result(
            round(weight * 0.25, 2),
            "weak",
            "analysis_payload",
            "Evidence is too fragmented for high-confidence documentation output.",
        )

    def _score_metadata_observability(
        self,
        context: dict[str, Any],
        weight: float,
        issues: list[dict[str, Any]],
    ) -> dict[str, Any]:
        limited_fields = 0
        for field_name in ("authentication", "protocols", "sender_systems", "receiver_systems"):
            values = context[field_name]
            if not self._has_confirmed_values(values):
                limited_fields += 1

        if limited_fields == 0:
            return self._dimension_result(
                weight,
                "strong",
                "analysis_payload",
                "Metadata observability is unexpectedly strong across the assessed dimensions.",
            )

        if limited_fields <= 2:
            return self._dimension_result(
                round(weight * 0.75, 2),
                "moderate",
                "analysis_payload",
                "Metadata-only observability is acceptable, with some expected visibility limits.",
            )

        issues.append(
            self._issue(
                anti_pattern_code="METADATA_OBSERVABILITY_LIMIT",
                category="Metadata Observability",
                severity="low",
                issue_type="visibility_limitation",
                points_deducted=round(weight * 0.4, 2),
                message="Metadata-only analysis exposes limited evidence across several technical dimensions.",
                recommendation="Use zip_based analysis for the final technical documentation set when deep evidence is required.",
            )
        )
        return self._dimension_result(
            round(weight * 0.6, 2),
            "limited",
            "analysis_payload",
            "Observability is constrained by metadata exposure and should be treated as a limitation rather than a defect.",
        )

    def _build_evidence_coverage(self, context: dict[str, Any]) -> dict[str, Any]:
        analysis_mode = context["analysis_mode"]
        signals = [
            self._coverage_signal("analysis_mode", [analysis_mode], analysis_mode),
            self._coverage_signal("authentication", context["authentication"], analysis_mode),
            self._coverage_signal("protocols", context["protocols"], analysis_mode),
            self._coverage_signal("sender_systems", context["sender_systems"], analysis_mode),
            self._coverage_signal("receiver_systems", context["receiver_systems"], analysis_mode),
            self._coverage_signal("package_name", [context["package_name"]] if context["package_name"] else [], analysis_mode),
            self._coverage_signal("resolved_version", [context["resolved_version"]] if context["resolved_version"] else [], analysis_mode),
            self._coverage_signal("summary", [context["summary"]] if context["summary"] else [], analysis_mode),
        ]

        percentage = round(sum(signal["coverage_value"] for signal in signals) / len(signals) * 100, 2)
        status = self._coverage_status_label(percentage)

        return {
            "percentage": percentage,
            "status": status,
            "signals": signals,
        }

    def _coverage_signal(self, field_name: str, values: list[str], analysis_mode: str) -> dict[str, Any]:
        if self._has_confirmed_values(values):
            return {
                "field": field_name,
                "status": "confirmed",
                "coverage_value": 1.0,
            }

        if analysis_mode == self.METADATA_ONLY_MODE and field_name in {
            "authentication",
            "protocols",
            "sender_systems",
            "receiver_systems",
        }:
            return {
                "field": field_name,
                "status": "limited",
                "coverage_value": 0.5,
            }

        if field_name == "summary" and values:
            return {
                "field": field_name,
                "status": "partial",
                "coverage_value": 0.5,
            }

        return {
            "field": field_name,
            "status": "missing",
            "coverage_value": 0.0,
        }

    def _build_confidence(
        self,
        analysis_mode: str,
        evidence_coverage_percentage: float,
    ) -> tuple[int, str]:
        mode_base = {
            self.ZIP_BASED_MODE: 85,
            self.METADATA_ONLY_MODE: 68,
            self.UNKNOWN_MODE: 55,
        }.get(analysis_mode, 55)

        confidence_score = int(round((mode_base * 0.6) + (evidence_coverage_percentage * 0.4)))

        if confidence_score >= 85:
            confidence_level = "very_high"
        elif confidence_score >= 72:
            confidence_level = "high"
        elif confidence_score >= 58:
            confidence_level = "medium"
        else:
            confidence_level = "low"

        return confidence_score, confidence_level

    def _build_anti_pattern_categories(self, issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, Any]] = {}

        for issue in issues:
            code = str(issue["anti_pattern_code"])
            if code not in grouped:
                grouped[code] = {
                    "anti_pattern_code": code,
                    "category": issue["category"],
                    "severity": issue["severity"],
                    "issue_type": issue["issue_type"],
                    "count": 0,
                    "points_deducted": 0.0,
                }
            grouped[code]["count"] += 1
            grouped[code]["points_deducted"] = round(
                grouped[code]["points_deducted"] + float(issue["points_deducted"]), 2
            )

        ordered = sorted(
            grouped.values(),
            key=lambda item: (
                self._severity_rank(item["severity"]),
                -float(item["points_deducted"]),
                item["anti_pattern_code"],
            ),
        )
        return ordered

    def _build_audit_output(
        self,
        iflow_id: str,
        context: dict[str, Any],
        final_score: int,
        confidence_level: str,
        confidence_score: int,
        evidence_coverage: dict[str, Any],
        anti_pattern_categories: list[dict[str, Any]],
    ) -> dict[str, Any]:
        analysis_mode = context["analysis_mode"]
        top_categories = anti_pattern_categories[:3]
        top_risks = [category["anti_pattern_code"] for category in top_categories]

        quality_gate = self._quality_gate(
            final_score=final_score,
            confidence_level=confidence_level,
            analysis_mode=analysis_mode,
        )

        return {
            "quality_gate": quality_gate,
            "documentation_ready": quality_gate in {"ready_for_publish", "ready_with_note"},
            "recommended_next_step": self._recommended_next_step(
                quality_gate=quality_gate,
                analysis_mode=analysis_mode,
            ),
            "top_risk_codes": top_risks,
            "mcp_documentation": {
                "iflow_id": iflow_id,
                "analysis_mode": analysis_mode,
                "score": final_score,
                "confidence_level": confidence_level,
                "confidence_score": confidence_score,
                "evidence_coverage_percentage": evidence_coverage["percentage"],
                "package_name": context["package_name"],
                "resolved_version": context["resolved_version"],
            },
            "audit_narrative": self._audit_narrative(
                iflow_id=iflow_id,
                analysis_mode=analysis_mode,
                final_score=final_score,
                confidence_level=confidence_level,
                evidence_coverage=evidence_coverage,
                top_risks=top_risks,
            ),
        }

    def _build_summary(
        self,
        iflow_id: str,
        context: dict[str, Any],
        final_score: int,
        confidence_level: str,
        evidence_coverage: dict[str, Any],
        issues: list[dict[str, Any]],
    ) -> str:
        analysis_mode = context["analysis_mode"]
        package_name = context["package_name"] or "not resolved"
        resolved_version = context["resolved_version"] or "not resolved"

        return (
            f"Enterprise scoring completed for {iflow_id} in {analysis_mode} mode with score "
            f"{final_score}/{self.max_score}. Confidence level: {confidence_level}. "
            f"Evidence coverage: {evidence_coverage['percentage']}% ({evidence_coverage['status']}). "
            f"Package: {package_name}. Version: {resolved_version}. "
            f"Detected issue count: {len(issues)}. "
            f"This output is formatted for MCP documentation and audit consumption."
        )

    def _quality_gate(
        self,
        final_score: int,
        confidence_level: str,
        analysis_mode: str,
    ) -> str:
        if final_score >= 85 and confidence_level in {"very_high", "high"}:
            return "ready_for_publish"
        if final_score >= 70:
            return "ready_with_note" if analysis_mode == self.METADATA_ONLY_MODE else "needs_review"
        return "needs_review"

    def _recommended_next_step(self, quality_gate: str, analysis_mode: str) -> str:
        if quality_gate == "ready_for_publish":
            return "Proceed with MCP documentation generation and attach the scoring matrix to the audit appendix."
        if quality_gate == "ready_with_note" and analysis_mode == self.METADATA_ONLY_MODE:
            return "Generate documentation with a visibility disclaimer, or re-run in zip_based mode for stronger technical evidence."
        return "Review the anti-pattern categories and strengthen parser evidence before publishing the technical documentation set."

    def _audit_narrative(
        self,
        iflow_id: str,
        analysis_mode: str,
        final_score: int,
        confidence_level: str,
        evidence_coverage: dict[str, Any],
        top_risks: list[str],
    ) -> str:
        risk_text = ", ".join(top_risks) if top_risks else "no dominant anti-patterns"
        return (
            f"The analyzed iFlow {iflow_id} achieved a score of {final_score}/{self.max_score} in "
            f"{analysis_mode} mode. Assessment confidence is {confidence_level}, supported by "
            f"evidence coverage of {evidence_coverage['percentage']}%. The most relevant audit focus areas are: {risk_text}."
        )

    def _detect_analysis_mode(self, analysis: dict[str, Any]) -> str:
        for key in ("analysis_mode", "mode", "parser_mode", "extraction_mode"):
            value = str(analysis.get(key, "")).strip().lower()
            if value in {self.ZIP_BASED_MODE, self.METADATA_ONLY_MODE}:
                return value

        summary = str(analysis.get("summary", "")).lower()
        if self.METADATA_ONLY_MODE in summary:
            return self.METADATA_ONLY_MODE
        if self.ZIP_BASED_MODE in summary:
            return self.ZIP_BASED_MODE

        return self.UNKNOWN_MODE

    def _mode_was_explicit(self, analysis: dict[str, Any]) -> bool:
        for key in ("analysis_mode", "mode", "parser_mode", "extraction_mode"):
            value = str(analysis.get(key, "")).strip().lower()
            if value in {self.ZIP_BASED_MODE, self.METADATA_ONLY_MODE}:
                return True
        return False

    def _get_scoring_profile(self, analysis_mode: str) -> str:
        if analysis_mode == self.ZIP_BASED_MODE:
            return "enterprise_full_content_confidence"
        if analysis_mode == self.METADATA_ONLY_MODE:
            return "enterprise_metadata_limited_confidence"
        return "enterprise_fallback_confidence"

    def _dimension_result(
        self,
        points_awarded: float,
        status: str,
        evidence_field: str,
        rationale: str,
    ) -> dict[str, Any]:
        return {
            "points_awarded": float(points_awarded),
            "status": status,
            "evidence_field": evidence_field,
            "rationale": rationale,
        }

    def _issue(
        self,
        anti_pattern_code: str,
        category: str,
        severity: str,
        issue_type: str,
        points_deducted: float,
        message: str,
        recommendation: str,
    ) -> dict[str, Any]:
        return {
            "anti_pattern_code": anti_pattern_code,
            "category": category,
            "severity": severity,
            "issue_type": issue_type,
            "points_deducted": float(points_deducted),
            "message": message,
            "recommendation": recommendation,
        }

    def _normalize_list(self, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, (tuple, set)):
            return [str(item).strip() for item in value if str(item).strip()]

        text = str(value).strip()
        return [text] if text else []

    def _first_non_empty(self, *values: Any) -> str:
        for value in values:
            text = str(value).strip()
            if text and text.lower() not in self.UNKNOWN_TOKENS:
                return text
        return ""

    def _has_confirmed_values(self, values: list[str]) -> bool:
        if not values:
            return False
        return any(not self._is_unknown_value(value) for value in values)

    def _is_unknown_value(self, value: str) -> bool:
        return str(value).strip().lower() in self.UNKNOWN_TOKENS

    def _severity_rank(self, severity: str) -> int:
        order = {"high": 0, "medium": 1, "low": 2}
        return order.get(str(severity).lower(), 3)

    def _coverage_status_label(self, percentage: float) -> str:
        if percentage >= 85:
            return "strong"
        if percentage >= 65:
            return "moderate"
        if percentage >= 45:
            return "limited"
        return "weak"
