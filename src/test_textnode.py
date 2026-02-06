import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_image, split_nodes_link, text_to_textnodes
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

    # def test_empty_segments_are_skipped(self):
    #     nodes = [TextNode("``code``", TextType.TEXT)]
    #     result = split_nodes_delimiter(nodes, "`", TextType.CODE)

    #     self.assertEqual(result, [
    #         TextNode("code", TextType.CODE),

    #     ])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    def test_full_markdown_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        nodes = text_to_textnodes(text)
        self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINK,
                "https://boot.dev",
            ),
        ],
        nodes,
        )

if __name__ == "__main__":
    unittest.main()