from textnode import TextNode, TextType
from htmlnode import HTMLNode
from aux_functions import split_nodes_delimiter

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

    text_node_1 = TextNode("Bunch of text without specials", TextType.TEXT)
    text_node_2 = TextNode("Bunch `code text` specials", TextType.TEXT)
    text_node_3 = TextNode("Bunch of text **without** specials", TextType.TEXT)
    text_node_4 = TextNode("Bunch _of text_ without specials", TextType.TEXT)
    text_node_5 = TextNode("`Bunch of _text_ without` specials", TextType.TEXT)
    text_node_6 = TextNode("Bunch _of text **without** specials_", TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node_1, text_node_2, text_node_3, text_node_4, text_node_5, text_node_6], "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    print(new_nodes)

main()
