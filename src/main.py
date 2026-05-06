from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)

    html_node_1 = HTMLNode(
                "a",
                "Anchor text",
                None,
                {
                    "href": "https://www.google.com",
                    "target": "_blank"
                }
            )
    html_node_2 = HTMLNode(
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
    print(html_node_1)
    print(html_node_2)

main()
