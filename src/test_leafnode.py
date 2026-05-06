import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq_plain(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node, "Plain text")

    def test_eq_p(self):
        node = LeafNode("p", "Paragraph text")
        self.assertEqual(node, "<p>Paragraph text</p>")

    def test_eq_b(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node, "<b>Bold text</b>")

    def test_eq_i(self):
        node = LeafNode("i", "Italics text")
        self.assertEqual(node, "<i>Italics text</i>")

    def test_eq_a(self):
        node = LeafNode("a", "Anchor text", {"href": "https://www.google.com"})
        self.assertEqual(node, '<a href="https://www.google.com">Anchor text</a>')
