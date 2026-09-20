import unittest

from blackmamba_netops.sentinel import EvidenceLedger, correlate
from blackmamba_netops.sentinel.sensors import ReadOnlySensor


class SentinelTests(unittest.TestCase):
    def test_ledger_is_epoch_scoped_and_hashed(self):
        ledger = EvidenceLedger("install-042")
        event = ledger.append(source="host", kind="socket", subject="pid:123", payload={"remote": "203.0.113.8:443"})
        exported = ledger.export()
        self.assertEqual(exported["epoch"], "install-042")
        self.assertEqual(exported["events"][0]["sha256"], event.digest)
        self.assertEqual(len(event.digest), 64)

    def test_two_independent_sources_are_corroborated(self):
        ledger = EvidenceLedger("install-042")
        ledger.append(source="host", kind="socket", subject="service:x", payload={})
        ledger.append(source="network", kind="flow", subject="service:x", payload={})
        finding = correlate(ledger.events())[0]
        self.assertEqual(finding.status, "corroborated")
        self.assertEqual(finding.evidence_count, 2)

    def test_sensor_contract_has_no_mutation_api(self):
        self.assertFalse(hasattr(ReadOnlySensor, "act"))
        self.assertFalse(hasattr(ReadOnlySensor, "mutate"))


if __name__ == "__main__":
    unittest.main()
