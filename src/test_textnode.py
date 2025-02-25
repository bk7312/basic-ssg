import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "website.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "website.comm")
        self.assertNotEqual(node, node2)
    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_not_eq3(self):
        node = TextNode("This is another text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_conv_text(self):
        node = TextNode("normal text", TextType.TEXT)
        self.assertEqual(node.text_node_to_html_node().to_html(), "normal text")

    def test_conv_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        self.assertEqual(node.text_node_to_html_node().to_html(), "<b>bold text</b>")

    def test_conv_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        self.assertEqual(node.text_node_to_html_node().to_html(), "<i>italic text</i>")

    def test_conv_code(self):
        node = TextNode("code text", TextType.CODE)
        self.assertEqual(node.text_node_to_html_node().to_html(), "<code>code text</code>")

    def test_conv_link(self):
        node = TextNode("link text", TextType.LINK, "link.com")
        self.assertEqual(node.text_node_to_html_node().to_html(), '<a href="link.com">link text</a>')
        
    def test_conv_image(self):
        node = TextNode("image text", TextType.IMAGE, "image.com")
        self.assertEqual(node.text_node_to_html_node().to_html(), '<img src="image.com" alt="image text"></img>')


if __name__ == "__main__":
    unittest.main()