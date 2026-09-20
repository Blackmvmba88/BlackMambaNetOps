import tempfile
import unittest
from pathlib import Path

from blackmamba_netops.sentinel.artifacts import identify
from blackmamba_netops.sentinel.bundle import write_bundle
from blackmamba_netops.sentinel.risk import score, signals
from blackmamba_netops.sentinel.sensors import SensorObservation


class RiskTests(unittest.TestCase):
    def test_docker_controls_are_explainable_signals(self):
        obs = SensorObservation("docker", "container", "container:x", {
            "privileged": True,
            "docker_socket_mounted": True,
            "port_bindings": {"8080/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]},
        })
        found = signals([obs])
        self.assertEqual(score("container:x", found), 9)
        self.assertEqual({s.rule for s in found}, {"docker.privileged", "docker.socket", "docker.public-bind"})

    def test_artifact_hash_and_bundle_sidecar(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            artifact = root / "sample.bin"
            artifact.write_bytes(b"blackmamba")
            identity = identify(artifact)
            self.assertEqual(len(identity.sha256), 64)
            sidecar, digest = write_bundle({"epoch": "install-043", "artifact": identity.sha256}, root / "evidence.json")
            self.assertTrue(sidecar.exists())
            self.assertIn(digest, sidecar.read_text())


if __name__ == "__main__":
    unittest.main()
