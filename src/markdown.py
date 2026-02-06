import re
from enum import Enum
from htmlnode import HtmlNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if block[:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE

    if block[0] == "#":
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(block) > count and block[count] == " ":
            return BlockType.HEADING

    if block[0] == ">":
        quoteBlock = block.split("\n")
        for line in quoteBlock:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block[:2] == "- ":
        unorderedBlock = block.split("\n")
        for line in unorderedBlock:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        orderedBlock = block.split("\n")
        count = 1
        for line in orderedBlock:
            if not line.startswith(f"{count}. "):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        blockType = block_to_block_type(block)
        if blockType == BlockType.PARAGRAPH:
            block_nodes.append(paragraph_to_html_node(block))
        elif blockType == BlockType.QUOTE:
            block_nodes.append(quote_to_html_node(block))
        elif blockType == BlockType.UNORDERED_LIST:
            block_nodes.append(unordered_list_to_html_node(block))
        elif blockType == BlockType.ORDERED_LIST:
            block_nodes.append(ordered_list_to_html_node(block))
        elif blockType == BlockType.CODE:
            block_nodes.append(code_to_html_node(block))
        elif blockType == BlockType.HEADING:
            block_nodes.append(heading_to_html_node(block))
    return HtmlNode("div", None, block_nodes)


def text_to_children(text):
    from textnode import text_to_textnodes, text_node_to_html_node
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]  
    children = text_to_children(text)
    return HtmlNode(f"h{level}", None, children)

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if line.startswith("> "):
            stripped_lines.append(line[2:])
        else:
            stripped_lines.append(line[1:]) 
    text = "\n".join(stripped_lines)
    children = text_to_children(text)
    return HtmlNode("blockquote", None, children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]  
        children = text_to_children(text)
        li_nodes.append(HtmlNode("li", None, children))
    return HtmlNode("ul", None, li_nodes)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for i, line in enumerate(lines):
        prefix = f"{i + 1}. "
        text = line[len(prefix):]
        children = text_to_children(text)
        li_nodes.append(HtmlNode("li", None, children))
    return HtmlNode("ol", None, li_nodes)

def code_to_html_node(block):
    text = block[4:-3]  
    from textnode import TextNode, TextType, text_node_to_html_node
    code_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
    code_wrapper = HtmlNode("code", None, [code_node])
    return HtmlNode("pre", None, [code_wrapper])

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return HtmlNode("p", None, children)






def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def markdown_to_blocks(markdown):
    textList = []
    splitMarkdown = markdown.split("\n\n")
    for string in splitMarkdown:
        lines = string.split("\n")
        stripped_lines = [line.strip() for line in lines]
        block = "\n".join(stripped_lines).strip()
        if block:
            textList.append(block)

    return textList

    










