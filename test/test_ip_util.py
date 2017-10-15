import unittest
from utils.ip_util import is_china_ip

class Test_ip_util(unittest.TestCase):
    def test_is_china_ip(self):
        result = is_china_ip('210.75.225.254')
        print result
        assert result == True
        result = is_china_ip('66.249.76.136')
        print result
        assert result == False


if __name__ == '__main__':
    unittest.main()