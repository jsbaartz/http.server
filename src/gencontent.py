import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def _normalize_basepath(basepath: str) -> str:
    # Ensure leading and trailing slash; "/" stays "/"
    if not basepath:
        return "/"
    if not basepath.startswith("/"):
        basepath = "/" + basepath
    if not basepath.endswith("/"):
        basepath = basepath + "/"
    return basepath

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    basepath = _normalize_basepath(basepath)
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            # Only convert markdown files
            if not filename.lower().endswith(".md"):
                continue
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath=basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath=basepath)

def generate_page(from_path, template_path, dest_path, basepath="/"):
    basepath = _normalize_basepath(basepath)
    print(f" * {from_path} {template_path} -> {dest_path}")

    from_file = open(from_path, "r", encoding="utf-8")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r", encoding="utf-8")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Base path rewriting for absolute-root links/assets
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/',  f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w", encoding="utf-8")
    to_file.write(page)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no title found")
