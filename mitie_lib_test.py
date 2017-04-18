import unittest

import mitie_lib

class MitieLibTestsTests(unittest.TestCase):

    def test_compare_simple_names(self):
        name1 = "Barack Obama"
        name2 = "Barack obama"
        self.failIf(not mitie_lib.compare_names(name1, name2))

    # def test_compare_partial_names(self):
    #     fullName = "Barack Obama"
    #     freeName = "barack"
    #     self.failIf(not mitie_lib.compare_names(fullName, freeName))
    #
    #     freeName = "obama"
    #     self.failIf(not mitie_lib.compare_names(fullName, freeName))

def main():
    unittest.main()

if __name__ == '__main__':
    main()