"""Integration helpers for hooking PoSE-PQC into omega-style pipelines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .pose_pqc import Evidence, PoSEPQC


class CoherenceEngine(Protocol):
    """Protocol expected from coherence engines that ingest evidences."""

    def record(self, evidence: Evidence) -> None:  # pragma: no cover - protocol
        ...


@dataclass
class OmegaIntegration:
    """Bridge between PoSE-PQC and an external coherence engine."""

    engine: CoherenceEngine
    psi_floor: float = 0.85

    def process_claim(self, pose: PoSEPQC, claim: str, psi: float, iti: str) -> bool:
        """Generate and forward evidence if it meets the floor.

        Returns ``True`` when evidence was produced and forwarded.
        """

        evidence = pose.generate_evidence(claim=claim, psi=psi, iti=iti)
        if evidence is None:
            return False

        if evidence.psi < self.psi_floor:
            return False

        self.engine.record(evidence)
        return True


__all__ = ["CoherenceEngine", "OmegaIntegration"]
