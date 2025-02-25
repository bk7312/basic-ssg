import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_missing_tag(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_missing_children(self):
        node = ParentNode(
            "p",
            None,
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_empty_children(self):
        node = ParentNode(
            "p",
            [],
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_children_not_list(self):
        node = ParentNode(
            "p",
            "test",
        )
        with self.assertRaises(ValueError):
            node.to_html()
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        text = node.to_html()
        # print(text)
        self.assertEqual(text, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_nested_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "nested Bold text"),
                        LeafNode(None, "nested Normal text"),
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "double nested Bold text"),
                                LeafNode(None, "double nested Normal text"),
                            ],
                        )
                    ],
                ),
                LeafNode(None, "Normal text"),
            ],
        )
        text = node.to_html()
        self.assertEqual(text, "<p><b>Bold text</b><p><b>nested Bold text</b>nested Normal text<p><b>double nested Bold text</b>double nested Normal text</p></p>Normal text</p>")



if __name__ == "__main__":
    unittest.main()