import json
import subprocess
import unittest

from blackmamba_netops.sentinel.docker import DockerSensor
from blackmamba_netops.sentinel.macos import MacOSHostSensor


def completed(argv, stdout="", returncode=0):
    return subprocess.CompletedProcess(argv, returncode, stdout, "")


class CollectorTests(unittest.TestCase):
    def test_macos_sensor_uses_no_shell_or_sudo(self):
        seen = []
        def runner(argv):
            seen.append(argv)
            return completed(argv, "ok")
        observations = MacOSHostSensor(runner).observe()
        self.assertEqual(len(observations), 7)
        self.assertTrue(all(isinstance(argv, list) for argv in seen))
        self.assertTrue(all("sudo" not in argv for argv in seen))

    def test_docker_surfaces_privilege_socket_and_ports(self):
        container = {
            "Id": "abcdef1234567890", "Name": "/watcher", "Config": {"Image": "example:latest"},
            "HostConfig": {"Privileged": True, "NetworkMode": "bridge", "PortBindings": {"8080/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8080"}]}},
            "Mounts": [{"Type": "bind", "Source": "/var/run/docker.sock", "Destination": "/var/run/docker.sock", "RW": True}],
        }
        def runner(argv):
            if argv[:2] == ["docker", "ps"]:
                return completed(argv, "abcdef1234567890\n")
            return completed(argv, json.dumps([container]))
        observations = DockerSensor(runner).observe()
        data = observations[1].payload
        self.assertTrue(data["privileged"])
        self.assertTrue(data["docker_socket_mounted"])
        self.assertIn("8080/tcp", data["port_bindings"])


if __name__ == "__main__":
    unittest.main()
