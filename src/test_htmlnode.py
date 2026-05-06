import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_simple(self):
        node = HTMLNode("p", "Paragraph text")
        node2 = HTMLNode("p", "Paragraph text")
        self.assertEqual(node, node2)

    def test_eq_with_children(self):
        node = HTMLNode(
                "ul",
                None,
                [
                    HTMLNode(
                        "li",
                        "Item 1"
                    ),
                    HTMLNode(
                        "li",
                        "Item 2"
                    )
                ]
            )
        node2 = HTMLNode(
                "ul",
                None,
                [
                    HTMLNode(
                        "li",
                        "Item 1"
                    ),
                    HTMLNode(
                        "li",
                        "Item 2"
                    )
                ]
            )
        self.assertEqual(node, node2)

    def test_eq_with_props(self):
        node = HTMLNode(
                "a",
                "Anchor text",
                None,
                {
                    "href": "https://www.google.com",
                    "target": "_blank"
                }
            )
        node2 = HTMLNode(
                "a",
                "Anchor text",
                None,
                {
                    "href": "https://www.google.com",
                    "target": "_blank"
                }
            )
        self.assertEqual(node, node2)

    def test_neq_simple(self):
        node = HTMLNode("p", "Paragraph text")
        node2 = HTMLNode(None, "Paragraph text")
        self.assertNotEqual(node, node2)

    def test_neq_simple_value_none(self):
        node = HTMLNode("p", None)
        node2 = HTMLNode("p", "None")
        self.assertNotEqual(node, node2)

    def test_neq_with_children(self):
        node = HTMLNode(
                "ul",
                None,
                [
                    HTMLNode(
                        "li",
                        "Item 1"
                    ),
                    HTMLNode(
                        "li",
                        "Item 2"
                    )
                ]
            )
        node2 = HTMLNode(
                "ul",
                None,
                [
                    HTMLNode(
                        "li",
                        "Item 1"
                    )
                ]
            )
        self.assertNotEqual(node, node2)

    def test_neq_with_props(self):
        node = HTMLNode(
                "a",
                "Anchor text",
                None,
                {
                    "href": "https://www.google.com",
                    "target": "_blank"
                }
            )
        node2 = HTMLNode(
                "a",
                "Anchor text",
                None,
                {
                    "href": "https://www.google.com"
                }
            )
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
