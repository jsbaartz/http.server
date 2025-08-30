# src/main.py
import os
import shutil
from typing import NoReturn


def copy_static_to_public(src: str = "static", dst: str = "public") -> NoReturn:
    """
    Recursively copy all contents of `src` into `dst`.
    - If `dst` exists, delete it first to ensure a clean build.
    - Recreate `dst`, then copy files and subdirectories, preserving structure.
    - Log each file copy for visibility.
    """
    if not os.path.exists(src):
        raise FileNotFoundError(
            f"Source directory '{src}' does not exist. "
            f"Make sure you created the 'static/' folder."
        )

    # Clean destination
    if os.path.exists(dst):
        print(f"Removing existing destination: {dst}")
        shutil.rmtree(dst)

    print(f"Creating destination: {dst}")
    os.makedirs(dst, exist_ok=True)

    def _copy_dir(src_dir: str, dst_dir: str) -> None:
        for name in os.listdir(src_dir):
            src_path = os.path.join(src_dir, name)
            dst_path = os.path.join(dst_dir, name)

            if os.path.isdir(src_path):
                # Recreate directory, then recurse
                os.makedirs(dst_path, exist_ok=True)
                print(f"[DIR ] {dst_path}")
                _copy_dir(src_path, dst_path)
            elif os.path.isfile(src_path):
                # Ensure parent exists (defensive), then copy
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(src_path, dst_path)
                print(f"[FILE] {src_path} -> {dst_path}")
            else:
                # Symlinks / special files skipped (unlikely in this project)
                print(f"[SKIP] {src_path} (not a regular file or directory)")

    _copy_dir(src, dst)


def main() -> NoReturn:
    copy_static_to_public()


if __name__ == "__main__":
    main()
