import unittest

from blackmamba_netops.core.intent import Intent, IntentDenied, IntentGate, Risk
from blackmamba_netops.core.management_link import ManagementLink
from blackmamba_netops.core.model import DeviceRecord
from blackmamba_netops.core.verify import act_and_verify


class CoreContracts(unittest.TestCase):
    def test_operator_annotation_never_overwrites_observation(self):
        d = DeviceRecord("mac:aa", observed={"hostname": "HONOR-X6a"})
        d.annotate("owner", "known")
        self.assertEqual(d.observed["hostname"], "HONOR-X6a")
        self.assertEqual(d.annotations["owner"], "known")

    def test_protected_intent_is_denied(self):
        with self.assertRaises(IntentDenied):
            IntentGate().authorize(Intent("write", Risk.PROTECTED, "gpon.loid"))

    def test_failed_readback_never_reports_success(self):
        result = act_and_verify(lambda: None, lambda: False, True)
        self.assertFalse(result.verified)

    def test_verified_ethernet_link_allows_radio_mutation(self):
        link = ManagementLink("192.168.100.1", "en7", "192.168.100.2", "ethernet", True)
        self.assertTrue(link.safe_for_radio_mutation)


if __name__ == "__main__":
    unittest.main()
