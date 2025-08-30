import re

_IMAGE_RE = re.compile(r'!\[([^\]]+)\]\(([^)\s]+)\)')

_LINK_RE = re.compile(r'(?<!!)\[([^\]]+)\]\(([^)\s]+)\)')

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches