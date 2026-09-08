#!/usr/bin/env python3
"""Portal Rubric Quality Check heuristics (mirrors Snorkel Section 2 automated checks)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PortalRubricFinding:
    criterion_id: str
    index: int
    severity: str  # "error" | "warn"
    check: str
    message: str


# Grade the upload package / golden archive, not the learner deliverable.
GOLDEN_ARCHIVE = re.compile(
    r"\bgolden solution (zip|archive)\b|\bgolden zip\b",
    re.I,
)
ZIP_ROOT_CRITERION = re.compile(
    r"\b(zip archive|submitted zip|golden solution zip)\b.*\b(at (the )?archive )?root\b",
    re.I,
)

# Grader notes, platform commentary, pasted scaffolding.
META_COMMENTARY = re.compile(
    r"\(platform accepted|platform accepts|criterion text:|^objective:|^subjective:|^style:",
    re.I,
)
GRADER_INSTRUCTION = re.compile(
    r"^(the grader|graders should|check whether the (candidate|submitter))\b",
    re.I,
)

# Process timing invisible in the deliverable — prefer document order on a tab/sheet.
PROCESS_TIMING = re.compile(
    r"\bbefore recommending\b|\bbefore (the )?board\b(?! sign-off recommendation)",
    re.I,
)

# Omission negatives risk dual-polarity with positive content checks.
OMISSION_NEGATIVE = re.compile(
    r"\b(does not|doesn't|fails to|is missing|omits|without (presenting|documenting|citing))\b",
    re.I,
)

# Prohibited-decision negatives should describe an affirmative bad recommendation.
PROHIBITED_DECISION = re.compile(
    r"\b(recommends|instructs|adopts|accepts|uses .+ as the (binding|final))\b",
    re.I,
)

WEIGHT_IN_TEXT = re.compile(
    r"\[\s*[+-]?\d+\s*\]|weight\s*[:\=]\s*[+-]?\d|\(\s*[+-]?\d+\s*points?\s*\)|\bworth\s+[+-]?\d+\b",
    re.I,
)


def _deliverable_as_source(text: str, deliverable: str) -> bool:
    if not deliverable:
        return False
    escaped = re.escape(deliverable)
    source_use = re.compile(
        rf"\b(from|per|in|using|according to)\s+{escaped}\b",
        re.I,
    )
    deliverable_use = re.compile(
        rf"\b(named|called|titled|file named|workbook named|deliverable is)\s+{escaped}\b",
        re.I,
    )
    return bool(source_use.search(text)) and not deliverable_use.search(text)


def portal_rubric_findings(
    criteria: Iterable[dict],
    *,
    deliverable_filename: str | None = None,
) -> list[PortalRubricFinding]:
    findings: list[PortalRubricFinding] = []
    deliverable = (deliverable_filename or "").strip()
    deliverable_is_zip = deliverable.lower().endswith(".zip")

    for i, c in enumerate(criteria, 1):
        cid = c.get("id", f"criterion_{i}")
        text = (c.get("text") or "").strip()
        weight = c.get("weight", 0)

        if WEIGHT_IN_TEXT.search(text):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "weight_in_text",
                    "Criterion text embeds a weight or point label — use the Weight field only.",
                )
            )

        if META_COMMENTARY.search(text):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "meta_commentary",
                    "Remove platform/grader meta-commentary from criterion text.",
                )
            )

        if GRADER_INSTRUCTION.search(text):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "grader_instruction",
                    "Criterion should state a checkable fact about the deliverable, not grader instructions.",
                )
            )

        if GOLDEN_ARCHIVE.search(text) or (
            not deliverable_is_zip and ZIP_ROOT_CRITERION.search(text)
        ):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "golden_archive",
                    "Do not grade golden.zip packaging — criteria must inspect the submitted deliverable only.",
                )
            )

        if PROCESS_TIMING.search(text):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "process_timing",
                    "Replace process-timing language with observable document order "
                    "(e.g. 'appears earlier on the Notes tab than …').",
                )
            )

        if deliverable and _deliverable_as_source(text, deliverable):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "deliverable_as_source",
                    f"Do not cite output file {deliverable} as a source — cite input files only.",
                )
            )

        if weight < 0 and weight not in (-3, -4, -5):
            findings.append(
                PortalRubricFinding(
                    cid, i, "error", "invalid_negative_weight",
                    f"Portal Rubric Structure Check rejects weight {weight}; "
                    f"negatives must be -3, -4, or -5 only (Ironclad: -7/-9 failed).",
                )
            )

        if weight < 0:
            if OMISSION_NEGATIVE.search(text) and not PROHIBITED_DECISION.search(text):
                findings.append(
                    PortalRubricFinding(
                        cid, i, "warn", "omission_negative",
                        "Negative may mirror a positive omission (penalty-scope risk). "
                        "Prefer an affirmative prohibited recommendation or decision.",
                    )
                )

    return findings
