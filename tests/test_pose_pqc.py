import hashlib
import hmac

from pose.pose_pqc import PoSEPQC


def test_generate_evidence_passes_threshold():
    pose = PoSEPQC(time_source=lambda: 123.0, signing_key=b"k" * 32)
    evidence = pose.generate_evidence("claim", 0.9, "iti")

    assert evidence is not None
    assert evidence.id == "EV-00000001"
    assert evidence.psi == 0.9
    assert evidence.timestamp == 123.0

    digest = hashlib.sha512("claim|0.900000|iti|123.000000000|1".encode()).digest()
    expected_signature = hmac.new(b"k" * 32, digest, hashlib.sha512).digest().hex()
    assert evidence.signature_hex == expected_signature


def test_generate_evidence_rejects_below_threshold():
    pose = PoSEPQC(psi_threshold=0.9)
    evidence = pose.generate_evidence("claim", 0.5, "iti")
    assert evidence is None


def test_generate_batch_respects_threshold_and_count():
    pose = PoSEPQC(time_source=lambda: 1.0)
    evidences = pose.generate_batch(
        count=5,
        claim="batch",
        base_psi=0.9,
        iti_seed="seed",
        psi_jitter=0.0,
    )
    assert len(evidences) == 5
    assert all(ev.claim == "batch" for ev in evidences)


