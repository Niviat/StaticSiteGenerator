import re

from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"{text_node.text_type} is not a valid type of TextNode")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_result = node.text.split(delimiter)
            
            if len(split_result) % 2 == 0:
                raise Exception(f"Closing delimiter '{delimiter}' is missing in text '{node.text}'")
            
            for idx in range(len(split_result)):
                if idx % 2 == 0 and len(split_result[idx]) != 0:
                    new_nodes.append(TextNode(split_result[idx], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_result[idx], text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches
    
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_to_split = node.text
            images = extract_markdown_images(node.text)

            if len(images) == 0:
                new_nodes.append(node)
            else:
                for image in images:
                    split_result = text_to_split.split(f"![{image[0]}]({image[1]})", 1)
                    if len(split_result[0]) != 0:
                        new_nodes.append(TextNode(split_result[0], TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    text_to_split = split_result[1]
                if len(text_to_split) != 0:
                    new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_to_split = node.text
            links = extract_markdown_links(node.text)

            if len(links) == 0:
                new_nodes.append(node)
            else:
                for link in links:
                    split_result = text_to_split.split(f"[{link[0]}]({link[1]})", 1)
                    if len(split_result[0]) != 0:
                        new_nodes.append(TextNode(split_result[0], TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    text_to_split = split_result[1]
                if len(text_to_split) != 0:
                    new_nodes.append(TextNode(text_to_split, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes
