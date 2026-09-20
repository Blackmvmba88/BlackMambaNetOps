import unittest

from blackmamba_netops.core.drift import diff
from blackmamba_netops.core.intent import Intent, Risk
from blackmamba_netops.core.management_link import ManagementLink
from blackmamba_netops.core.model import DeviceRecord
from blackmamba_netops.core.policy import PolicyEngine
from blackmamba_netops.core.topology import Topology


class AdaptiveContracts(unittest.TestCase):
    def test_radio_write_requires_verified_wired_path(self):
        intent = Intent("wifi.radio.write", Risk.MUTATE, "radio:2.4", False)
        wifi = ManagementLink("192.168.100.1", "en0", "192.168.100.2", "wifi", True)
        ethernet = ManagementLink("192.168.100.1", "en7", "192.168.100.2", "ethernet", True)
        self.assertFalse(PolicyEngine().evaluate(intent, wifi).allowed)
        self.assertTrue(PolicyEngine().evaluate(intent, ethernet).allowed)

    def test_drift_is_descriptive_not_accusatory(self):
        changes = diff({"hostname": "A", "online": False}, {"hostname": "A", "online": True})
        self.assertEqual([(d.key, d.before, d.after) for d in changes], [("online", False, True)])

    def test_topology_requires_evidence_for_relation(self):
        a, b = DeviceRecord("router"), DeviceRecord("phone")
        t = Topology()
        t.ingest([a, b])
        t.relate("phone", "router", "associated-with", "router client table")
        self.assertEqual(t.edges[0].evidence, "router client table")


if __name__ == "__main__":
    unittest.main()
