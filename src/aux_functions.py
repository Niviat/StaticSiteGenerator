import re
from enum import Enum

from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode

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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    sanitized_blocks = []

    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            sanitized_blocks.append(block)
    
    return sanitized_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"

def block_to_block_type(md_block):
    block_type = BlockType.PARAGRAPH

    if re.match(r"#{1,6} ", md_block):
        block_type = BlockType.HEADING
    elif re.match(r"`{3}\n.*\n`{3}$", md_block, re.S):
        block_type = BlockType.CODE
    elif all(list(map(lambda x: True if x == "" or re.match(r">", x) else False, md_block.split("\n")))):
        block_type = BlockType.QUOTE
    elif all(list(map(lambda x: True if x == "" or re.match(r"- ", x) else False, md_block.split("\n")))):
        block_type = BlockType.ULIST
    else:
        lines = md_block.split("\n")
        idx = 1
        ordered = True

        for line in lines:
            match = re.match(r"[1-9]\d*\. ", line)
            if match:
                if int(match.group()[0:-2]) != idx:
                    ordered = False
                    break
            elif line != "":
                ordered = False
                break
            idx += 1
        
        if ordered:
            block_type = BlockType.OLIST

    return block_type

def text_to_leaf_nodes(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []

    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    
    return leaf_nodes

def block_to_html_node(block_type, block):
    block_lines = block.split("\n")
    match block_type:
        case BlockType.PARAGRAPH:
            content = " ".join(list(map(lambda x: x.strip(), block_lines)))
            leaf_nodes = text_to_leaf_nodes(content)
            return ParentNode("p", leaf_nodes)
        case BlockType.HEADING:
            level = 0
            while block_lines[0][level] == "#":
                level += 1
            block_lines[0] = block_lines[0][level:]
            content = " ".join(list(map(lambda x: x.strip(), block_lines)))
            leaf_nodes = text_to_leaf_nodes(content)
            return ParentNode(f"h{level}", leaf_nodes)
        case BlockType.CODE:
            content = block[4:-3]
            leaf_nodes = [text_node_to_html_node(TextNode(content, TextType.CODE))]
            return ParentNode("pre", leaf_nodes)
        case BlockType.QUOTE:
            content = " ".join(list(map(lambda x: x[1:].strip(), block_lines)))
            leaf_nodes = text_to_leaf_nodes(content)
            return ParentNode("blockquote", leaf_nodes)
        case BlockType.ULIST:
            li_nodes = []
            for line in block_lines:
                content = line[1:].strip()
                leaf_nodes = text_to_leaf_nodes(content)
                li_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ul", li_nodes)
        case BlockType.OLIST:
            li_nodes = []
            for idx in range(len(block_lines)):
                content = block_lines[idx][len(f"{idx}."):].strip()
                leaf_nodes = text_to_leaf_nodes(content)
                li_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ol", li_nodes)
        case _:
            content = " ".join(block_lines.strip())
            leaf_nodes = text_to_leaf_nodes(content)
            return ParentNode("div", leaf_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_nodes.append(block_to_html_node(block_type, block))
    
    return ParentNode("div", block_nodes)
