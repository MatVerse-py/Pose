"""PoSE-PQC evidence generation utilities.

This module keeps the API surface small and dependency-free while
exposing extension points for future post-quantum backends such as
Dilithium. By default it relies on HMAC-SHA-512 to produce signatures,
which makes the module runnable without external libraries in
constrained CI environments.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import secrets
import time
from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Optional


def _now() -> float:
    return time.time()


@dataclass
class Evidence:
    """Represents an immutable evidence note produced by PoSE-PQC."""

    id: str
    claim: str
    psi: float
    iti: str
    timestamp: float
    hash_hex: str
    signature_hex: str
    public_key_hex: str
    omega_validated: float

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


class PoSEPQC:
    """Proof of Semantic Existence (PoSE) with a PQC-friendly API.

    The implementation is intentionally dependency-light. It uses
    HMAC-SHA-512 for signatures while exposing clear seams to plug in a
    Dilithium (or other PQC) signer in the future.
    """

    def __init__(
        self,
        psi_threshold: float = 0.85,
        time_source: Callable[[], float] = _now,
        signing_key: Optional[bytes] = None,
    ) -> None:
        self.psi_threshold = psi_threshold
        self.time_source = time_source
        self.private_key = signing_key or secrets.token_bytes(32)
        self.public_key = hashlib.sha256(self.private_key).digest()
        self._counter = 0

    def _hash_evidence(self, claim: str, psi: float, iti: str, ts: float) -> bytes:
        payload = f"{claim}|{psi:.6f}|{iti}|{ts:.9f}|{self._counter}".encode()
        return hashlib.sha512(payload).digest()

    def _sign(self, digest: bytes) -> bytes:
        return hmac.new(self.private_key, digest, hashlib.sha512).digest()

    def generate_evidence(self, claim: str, psi: float, iti: str) -> Optional[Evidence]:
        """Generate a single evidence note if ``psi`` meets the threshold.

        Args:
            claim: Human-readable claim being attested.
            psi: Semantic coherence score for the claim.
            iti: Immutable Trace Identifier for the producing agent.

        Returns:
            Evidence if ``psi`` passes the threshold; otherwise ``None``.
        """

        if not math.isfinite(psi):
            return None

        if psi < self.psi_threshold:
            return None

        self._counter += 1
        ts = self.time_source()
        digest = self._hash_evidence(claim=claim, psi=psi, iti=iti, ts=ts)
        signature = self._sign(digest)

        evidence = Evidence(
            id=f"EV-{self._counter:08d}",
            claim=claim,
            psi=round(psi, 6),
            iti=iti,
            timestamp=ts,
            hash_hex=digest.hex(),
            signature_hex=signature.hex(),
            public_key_hex=self.public_key.hex(),
            omega_validated=round((psi + (1 - 0.007)) / 2, 6),
        )
        return evidence

    def generate_batch(
        self,
        count: int,
        claim: str,
        base_psi: float,
        iti_seed: str,
        psi_jitter: float = 0.001,
    ) -> List[Evidence]:
        """Generate a batch of evidence notes.

        The batch API keeps computation lightweight while still matching
        the shape required by downstream systems that expect large
        volumes (e.g., 100k notes). Jitter is applied to introduce
        minimal diversity in ``psi`` values.
        """

        evidences: List[Evidence] = []
        for i in range(count):
            psi = base_psi + ((i % 100) * psi_jitter)
            iti = hashlib.sha256(f"{iti_seed}:{i}".encode()).hexdigest()
            evidence = self.generate_evidence(claim=claim, psi=psi, iti=iti)
            if evidence:
                evidences.append(evidence)
        return evidences


__all__ = ["Evidence", "PoSEPQC"]
