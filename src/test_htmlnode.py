import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        node = HTMLNode("a", "link")
        self.assertEqual(repr(node), "HTMLNode(a, link, None, None)")
    def test_to_html(self):
        node = HTMLNode("a", "link")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        text = node.props_to_html()
        self.assertEqual(text, ' href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()