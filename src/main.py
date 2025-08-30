import os
import sys
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"        # build into docs/ for GitHub Pages
dir_path_content = "./content"
template_path = "./template.html"

def main():
    # Basepath from CLI (default "/")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting docs directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print(f"Generating content (basepath: {basepath})...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath=basepath)

if __name__ == "__main__":
    main()
