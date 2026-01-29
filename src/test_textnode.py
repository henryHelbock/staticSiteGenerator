import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node.url)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsInstance(node.text_type, TextType)

    def test_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsInstance(node.text, str)


if __name__ == "__main__":
    unittest.main()