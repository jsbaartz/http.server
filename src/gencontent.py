import re
import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            # only convert markdown
            if not filename.lower().endswith(".md"):
                continue
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath=basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath=basepath)

def _normalize_basepath(basepath: str) -> str:
    if not basepath:
        return "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath += "/"
    return basepath

def _fix_internal_links_trailing_slash(page_html: str, basepath: str) -> str:
    """
    Ensure internal links point to directory indexes by adding a trailing '/' when:
      - href starts with the basepath
      - and does NOT already end with '/' 
      - and does NOT point to a file with an extension (e.g., .html, .png, .css)
    """
    def needs_slash(url: str) -> bool:
        if not url.startswith(basepath):
            return False
        if url.endswith("/"):
            return False
        last = url.split("/")[-1]
        if "." in last:  # has extension -> leave it alone
            return False
        return True

    def repl(m):
        url = m.group(1)
        if needs_slash(url):
            return f'href="{url}/"'
        return m.group(0)

    return re.sub(r'href="([^"]+)"', repl, page_html)


def generate_page(from_path, template_path, dest_path, basepath="/"):
    basepath = _normalize_basepath(basepath)
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Rewrite absolute-root URLs to use the basepath
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/',  f'src="{basepath}')

    # Add trailing slash to internal links so /path/ resolves to index.html on GitHub Pages
    page = _fix_internal_links_trailing_slash(page, basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)
def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")
