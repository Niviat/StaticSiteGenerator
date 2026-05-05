from textnode import *

def main():
    t_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(t_node)

main()
