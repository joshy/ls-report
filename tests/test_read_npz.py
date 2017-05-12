import unittest
from lsreport.read_npz import _parse_acc_number


class TestParseAccNumber(unittest.TestCase):
    def test_parsing(self):
        dir_name = 'asdf123235ACC123456789'
        acc_number = _parse_acc_number(dir_name)
        self.assertEqual('123456789', acc_number)
