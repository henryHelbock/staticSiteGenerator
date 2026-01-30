import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from delimiters import split_nodes_delimiter

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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_no_delimiter(self):
        nodes = [TextNode("Just plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, nodes)

    def test_single_code_delimiter(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_code_delimiters(self):
        nodes = [TextNode("`a` and `b`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("a", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.CODE),
        ])

    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, nodes)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("This is `broken text", TextType.TEXT)]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_empty_segments_are_skipped(self):
        nodes = [TextNode("``code``", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
        ])

if __name__ == "__main__":
    unittest.main()