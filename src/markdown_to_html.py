# src/markdown_to_html.py
from htmlnode import ParentNode, LeafNode
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def text_to_children(text: str):
    """
    Convert inline markdown text into a list of HTMLNode children using the
    inline pipeline: text -> [TextNode...] -> [HTMLNode...]
    """
    tnodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in tnodes]


def _parse_paragraph(block: str) -> ParentNode:
    # Merge consecutive lines inside a paragraph block with single spaces
    merged = " ".join(line.strip() for line in block.split("\n")).strip()
    return ParentNode("p", text_to_children(merged))


def _parse_heading(block: str) -> LeafNode:
    # Block already guaranteed to start with 1..6 hashes + space
    first_line = block.split("\n", 1)[0]
    hashes, content = first_line.split(" ", 1)
    level = min(len(hashes), 6)
    return LeafNode(f"h{level}", content.strip())


def _parse_code(block: str) -> ParentNode:
    # Fenced code block: keep content verbatim, no inline parsing.
    lines = block.split("\n")
    inner = "\n".join(lines[1:-1]) + "\n"  # preserve trailing newline per test
    return ParentNode("pre", [LeafNode("code", inner)])


def _parse_quote(block: str) -> ParentNode:
    # Strip a single leading '>' (and one optional space) from each non-blank line
    cleaned_lines = []
    for line in block.split("\n"):
        if not line.strip():
            continue
        s = line.lstrip()
        if s.startswith(">"):
            s = s[1:]
            if s.startswith(" "):
                s = s[1:]
        cleaned_lines.append(s.rstrip())
    merged = " ".join(cleaned_lines).strip()
    return ParentNode("blockquote", text_to_children(merged))


def _parse_ulist(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if not line.strip():
            continue
        # line starts with "- "
        content = line[2:] if line.startswith("- ") else line.lstrip()[2:]
        items.append(ParentNode("li", text_to_children(content.rstrip())))
    return ParentNode("ul", items)


def _parse_olist(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if not line.strip():
            continue
        # consume "N. " prefix
        stripped = line.lstrip()
        dot_idx = stripped.find(". ")
        content = stripped[dot_idx + 2 :] if dot_idx != -1 else stripped
        items.append(ParentNode("li", text_to_children(content.rstrip())))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert a full markdown document into a single <div> ParentNode
    containing child HTMLNodes for each block (paragraphs, headings,
    code blocks, quotes, ordered/unordered lists).
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        btype = block_to_block_type(block)
        if btype == BlockType.PARAGRAPH:
            children.append(_parse_paragraph(block))
        elif btype == BlockType.HEADING:
            children.append(_parse_heading(block))
        elif btype == BlockType.CODE:
            children.append(_parse_code(block))
        elif btype == BlockType.QUOTE:
            children.append(_parse_quote(block))
        elif btype == BlockType.ULIST:
            children.append(_parse_ulist(block))
        elif btype == BlockType.OLIST:
            children.append(_parse_olist(block))
        else:
            # Fallback as paragraph
            children.append(_parse_paragraph(block))
    return ParentNode("div", children)
