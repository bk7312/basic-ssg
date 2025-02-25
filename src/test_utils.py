import unittest

from utils import *
from leafnode import *

class TestUtils(unittest.TestCase):
    maxDiff = None
    def test_split_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_split_multi_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node, node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
        

    def test_split_text_2(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]

        self.assertEqual(new_nodes, expected)
    def test_split_text_2(self):
        node = TextNode("`This is code` with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is code", TextType.CODE),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE)
        ]

        self.assertEqual(new_nodes, expected)

    def test_split_text_3(self):
        node = TextNode("This `is` text `with` a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.CODE),
            TextNode(" text ", TextType.TEXT),
            TextNode("with", TextType.CODE),
            TextNode(" a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    def test_split_non_text(self):
        node = TextNode("This is text with a `code block`", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a `code block`", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)

    def test_incomplete_markdown(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)

        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_incomplete_markdown_2(self):
        node = TextNode("This `is` text with a `code block", TextType.TEXT)

        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expect = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expect)
        
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expect = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expect)

    def test_split_images(self):
        node = TextNode(
            "This is image with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expect = [
            TextNode("This is image with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_image([node]), expect)

    def test_split_images_multi(self):
        node = TextNode(
            "This is image with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        expect = [
            TextNode("This is image with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(split_nodes_image([node, node1, node2]), expect)

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        expect = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_link([node]), expect)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expect = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expect)


    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expect = [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        self.assertEqual(markdown_to_blocks(text), expect)


    def test_markdown_to_blocks(self):
        text = """# This is a heading    

        

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.   


   * This is the first list item in a list block
* This is a list item
* This is another list item"""
        expect = [
            "# This is a heading", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        self.assertEqual(markdown_to_blocks(text), expect)
        
    def test_is_heading(self):
        text = "#### test"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
    def test_is_not_heading(self):
        text = "####### test"
        self.assertNotEqual(block_to_block_type(text), BlockType.HEADING)

    def test_is_code(self):
        text = "```code```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    def test_is_not_code(self):
        text = "``what``"
        self.assertNotEqual(block_to_block_type(text), BlockType.CODE)

    def test_is_quote(self):
        text = """> quote\n> another"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    def test_is_not_quote(self):
        text = ">not\nquote"
        self.assertNotEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_is_unordered_list(self):
        text = "* t\n* p"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)
    def test_is_not_unordered_list(self):
        text = "* f\nrte"
        self.assertNotEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_is_ordered_list(self):
        text = "1. t\n2. p"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)
    def test_is_not_ordered_list(self):
        text = "2. f\n3.rte"
        self.assertNotEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_is_paragraph(self):
        text = "1. t\n- p"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_markdown_to_html(self):
        markdown = "## heading 2\n\nthis is **a** paragraph\n\na double line\nparagraph double."
        output = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h2", [
                LeafNode(None, "heading 2"),
            ]),
            ParentNode("p", [
                LeafNode(None, "this is "),
                LeafNode("b", "a"),
                LeafNode(None, " paragraph"),
            ]),
            ParentNode("p", [
                LeafNode(None, "a double line\nparagraph double."),
            ]),
        ])
        self.assertEqual(repr(output), repr(expected))

    def test_markdown_to_html_2(self):
        markdown = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is "),
                LeafNode("b", "text"),
                LeafNode(None, " with an "),
                LeafNode("i", "italic"),
                LeafNode(None, " word and a "),
                LeafNode("code", "code block"),
                LeafNode(None, " and an "),
                LeafNode("img", "", {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href": "https://boot.dev"}),
            ]),
        ])
        self.assertEqual(repr(output), repr(expected))

    def test_markdown_to_html_code_quote(self):
        markdown = "Test 3\n\n```some code\nhow fun```\n\n> what did the fox say\n> skittles\n\nend of test"
        output = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Test 3"),
            ]),
            ParentNode("pre", [
                ParentNode("code", [
                    LeafNode(None, "some code\nhow fun"),
                ]),
            ]),
            ParentNode("blockquote", [
                ParentNode("p",[
                    LeafNode(None, "what did the fox say"),
                ]),
                ParentNode("p",[
                    LeafNode(None, "skittles"),
                ]),
            ]),
            ParentNode("p", [
                LeafNode(None, "end of test"),
            ]),
        ])
        self.assertEqual(repr(output), repr(expected))

    def test_markdown_to_html_lists(self):
        markdown = "Test 4\n\n1. list\n2. of\n3. orders\n\n- list\n* of\n- unorders"
        output = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Test 4"),
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "of"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "orders"),
                ]),
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "list"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "of"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "unorders"),
                ]),
            ]),
        ])
        self.assertEqual(repr(output), repr(expected))
    

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
    def test_extract_title_2(self):
        self.assertEqual(extract_title("# Hello world"), "Hello world")
    def test_extract_title_3(self):
        with self.assertRaises(Exception):
            extract_title("## Hello world")
    def test_extract_title_4(self):
        with self.assertRaises(Exception):
            extract_title("##Hello world")
    def test_extract_title_5(self):
        with self.assertRaises(Exception):
            extract_title("#")
    def test_extract_title_6(self):
        with self.assertRaises(Exception):
            extract_title("not a title")

if __name__ == "__main__":
    unittest.main()