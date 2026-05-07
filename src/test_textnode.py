import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_simple(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Anchor text", TextType.LINK, "https://www.google.com")
        node2 = TextNode("Anchor text", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_neq_simple(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("Anchor text", TextType.LINK, "https://www.google.com")
        node2 = TextNode("Anchor text", TextType.IMAGE, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_neq_url_None(self):
        node = TextNode("Anchor text", TextType.LINK)
        node2 = TextNode("Anchor text", TextType.LINK, "")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
