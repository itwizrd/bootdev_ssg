import re
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split('\n')
    if re.match(r'#{1,6} .+', block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):#if re.match(r'```.*```', block, re.DOTALL):
        return BlockType.CODE
    if block.startswith('>'):
        for line in lines:
            if not line.startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith('* ') or block.startswith('- '):
        for line in lines:
            if not (line.startswith('* ') or line.startswith('- ')):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith('1. '):
        i = 1
        for line in lines:
            if not line.startswith(f'{i}. '):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if block_type == BlockType.HEADING:
        return heading_to_html(block)
    if block_type == BlockType.CODE:
        return code_to_html(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html(block)
    if block_type == BlockType.OLIST:
        return olist_to_html(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html(block)
    raise ValueError("invalid BlockType")

def paragraph_to_html(block):
    lines = block.split('\n')
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid BlockType.CODE")
    text = block[4:-3]
    raw_text = TextNode(text, TextType.TEXT)
    children = text_node_to_html_node(raw_text)
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])

def quote_to_html(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid BlockType.QUOTE")
        new_lines.append(line.lstrip("> "))
    quote = " ".join(new_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)

def olist_to_html(block):
    lines = block.split('\n')
    list_items = []
    for item in lines:
        text = re.sub(r"\d+\.\s", "", item)
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)

def ulist_to_html(block):
    lines = block.split('\n')
    list_items = []
    for item in lines:
        text = re.sub(r"[\*\-]\s", "", item)
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)
