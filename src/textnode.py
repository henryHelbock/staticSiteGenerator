from enum import Enum

from htmlnode import LeafNode
from markdown import extract_markdown_images, extract_markdown_links
from delimiters import split_nodes_delimiter

class TextType(Enum):
    TEXT = "text"
    BOLD = "BOLD"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"



class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return( self.text == other.text and self.text_type == other.text_type and self.url == other.url)
    
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type.value}, {self.url})")
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise Exception("not an instance of text type")
    else:
        if text_node.text_type == TextType.TEXT:
            node = LeafNode(None, text_node.text)
            return node

        if text_node.text_type == TextType.BOLD:
            node = LeafNode("b", text_node.text)
            return node

        if text_node.text_type == TextType.ITALIC:
            node = LeafNode("i", text_node.text)
            return node
        
        if text_node.text_type == TextType.CODE:
            node = LeafNode("code", text_node.text)
            return node
        
        if text_node.text_type == TextType.LINK:
            node = LeafNode("a", text_node.text, props={"href" : text_node.url})
            return node
        
        if text_node.text_type == TextType.IMAGE:
            node = LeafNode("img", "", props={"src" : text_node.url, "alt" : text_node.text})
            return node
    

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            image_md = f"![{alt}]({url})"
            before, text = text.split(image_md, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for anchor, url in links:
            link_md = f"[{anchor}]({url})"
            before, text = text.split(link_md, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        # leftover text after last link
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


            
            

