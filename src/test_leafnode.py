import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_print(self):
        node = LeafNode(None, "link")
        self.assertEqual(repr(node), "HTMLNode(None, link, None, None)")
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        text = node.to_html()
        # print(text)
        self.assertEqual(text, "<p>This is a paragraph of text.</p>")
    def test_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        text = node.to_html()
        self.assertEqual(text, '<a href="https://www.google.com">Click me!</a>')
    def test_to_html_3(self):
        node = LeafNode(None, "plain text")
        text = node.to_html()
        self.assertEqual(text, "plain text")
    def test_to_html_4(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()



if __name__ == "__main__":
    unittest.main()