import unittest

import banditvis

class FirstTest(unittest.TestCase):
    def test_is_string(self):
        s = "superhappystring"
        self.assertTrue(isinstance(s, int))

if __name__ == "__main__":
    unittest.main()