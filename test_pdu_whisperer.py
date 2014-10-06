import unittest
import pdu_whisperer

class TestPduWhisperer(unittest.TestCase):
    def setUp(self):
        self.whisperer = PduWhisperer()
        self.pdus = ('pdu-b210-dell65.osuosl.oob',)

    def test_get_outlet_power_state(self):
        print self.whisperer(self.pdus)

    def test_turn_outlet(self):
        # Turn off outlet 0
        whisperer.turn_off_outlet(self.pdus[0], 0)
        # Asset that it's off
        self.assertTrue(whisperer.outletStatus(self.pdus[0], 0) == 2)
        whisperer.turn_on_outlet(self.pdus[0], 0)
        # Assert that the outlet is on
        self.assertTrue(whisperer.outletStatus(self.pdus[0], 0) == 1)
        whisperer.turn_off_outlet(self.pdus[0], 0)
        # Asset that it's off again
        self.assertTrue(whisperer.outletStatus(self.pdus[0], 0) == 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
