import unittest

import mitie_lib

class MitieLibTests(unittest.TestCase):

    def test_compare_simple_names(self):
        name1 = "Barack Obama"
        name2 = "Barack obama"
        self.failIf(not mitie_lib.compare_names(name1, name2))

    def test_extract_text_by_xrange_with_offset(self):
        original_text = "mid-brown volumes of the EETS, with the symbol of Alfred's jewel"
        tokens = mitie_lib.tokenize_with_offsets(original_text)
        extracted_text = mitie_lib.extract_text_by_xrange_with_offset(tokens, range(len(tokens)))
        self.failUnlessEqual(original_text, extracted_text)


def main():
    unittest.main()

if __name__ == '__main__':
    main()