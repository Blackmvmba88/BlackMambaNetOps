import unittest

from blackmamba_netops.sentinel.epochs import compare_epochs
from blackmamba_netops.sentinel.normalize import parse_lsof_sockets


class NormalizeTests(unittest.TestCase):
    def test_process_socket_remote_edge(self):
        sample = "curl 4242 user 5u IPv4 0x0 0t0 TCP 192.168.1.2:50000->203.0.113.8:443 (ESTABLISHED)"
        edge = parse_lsof_sockets(sample)[0]
        self.assertEqual(edge.pid, 4242)
        self.assertEqual(edge.remote, "203.0.113.8:443")
        self.assertEqual(edge.state, "ESTABLISHED")

    def test_cross_epoch_reappearance(self):
        event = {"source": "macos.persistence", "kind": "launch_item", "subject": "file:/x.plist", "payload": {"size": 10}}
        changes = compare_epochs({"events": [event]}, {"events": [event]})
        self.assertEqual(changes[0].status, "reappeared")

    def test_cross_epoch_appearance(self):
        event = {"source": "macos.persistence", "kind": "launch_item", "subject": "file:/new.plist", "payload": {}}
        changes = compare_epochs({"events": []}, {"events": [event]})
        self.assertEqual(changes[0].status, "appeared")


if __name__ == "__main__":
    unittest.main()
