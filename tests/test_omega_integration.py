from pose.omega_integration import OmegaIntegration
from pose.pose_pqc import PoSEPQC


class Recorder:
    def __init__(self):
        self.seen = []

    def record(self, evidence):
        self.seen.append(evidence)


def test_process_claim_accepts_and_records():
    recorder = Recorder()
    omega = OmegaIntegration(engine=recorder)
    pose = PoSEPQC(time_source=lambda: 1.0)

    assert omega.process_claim(pose, claim="ok", psi=0.95, iti="iti") is True
    assert len(recorder.seen) == 1


def test_process_claim_rejects_low_score():
    recorder = Recorder()
    omega = OmegaIntegration(engine=recorder, psi_floor=0.9)
    pose = PoSEPQC(time_source=lambda: 1.0, psi_threshold=0.8)

    assert omega.process_claim(pose, claim="low", psi=0.85, iti="iti") is False
    assert recorder.seen == []
