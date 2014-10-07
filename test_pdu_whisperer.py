import unittest
from pdu_whisperer import PduWhisperer, Outlet

class TestPduWhisperer(unittest.TestCase):
    def setUp(self):
        self.whisperer = PduWhisperer()
        self.pdus = ('pdu-b210-dell65.osuosl.oob',)

    def test_get_outlet_power_state(self):
        print self.whisperer.scan_pdus(self.pdus)

    def test_turn_outlet(self):
        outlet = Outlet(0, 0, 0)
        # Turn off outlet 0
        self.whisperer.turn_off_outlet(self.pdus[0], outlet)
        # Asset that it's off
        self.assertEqual(self.whisperer.outlet_status(self.pdus[0], outlet), 2)
        self.whisperer.turn_on_outlet(self.pdus[0], outlet)
        # Assert that the outlet is on
        self.assertEqual(self.whisperer.outlet_status(self.pdus[0], outlet), 1)
        self.whisperer.turn_off_outlet(self.pdus[0], outlet)
        # Asset that it's off again
        self.assertEqual(self.whisperer.outlet_status(self.pdus[0], outlet), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
