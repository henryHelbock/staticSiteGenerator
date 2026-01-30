import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("a", "link", props={"href": "https://example.com", "target": "_blank"})
        html = node.props_to_html()
        self.assertIn('href=https://example.com', html)
        self.assertIn('target=_blank', html)

    def test_props_to_html_empty(self):
        node = HtmlNode("p", "hello")
        html = node.props_to_html()

        self.assertEqual(html, "")

    def test_constructor_sets_values(self):
        node = HtmlNode("p", "hello")

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href=https://example.com>Hello, world!</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()