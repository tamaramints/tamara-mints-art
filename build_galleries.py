#!/usr/bin/env python3
import os
import subprocess
import urllib.parse

SRC_ROOT = "/Users/tamara/Desktop/portfolio"
PROJECT_ROOT = "/Users/tamara/Desktop/AI агенты/Tamara Mints Art"
MAX_DIM = 1100

IMG_EXTS = {".jpg", ".jpeg", ".png"}

GALLERY_CATEGORIES = [
    ("AVANT-GARDE", "avant-garde", "Avant-Garde"),
    ("NEO-EXPRESSIONISM", "neo-expressionism", "Neo-Expressionism"),
    ("CLASSICAL", "classical", "Classical"),
    ("ILLUSTRATIONS", "illustrations", "Illustrations"),
    ("EXHIBITIONS", "exhibitions", "Exhibitions"),
    ("KERAMIKA", "keramika", "Keramika"),
    ("HOME", "additional-works", "Additional Works"),
]

DESIGN_CATEGORIES = [
    ("GRAPHIC DESIGNER", "graphic-designer", "Graphic Designer"),
    ("PRODUCT DESIGN", "product-design", "Product Design"),
    ("DIGITAL ILLUSTRATION", "digital-illustration", "Digital Illustration"),
    ("PHOTOSHOP", "photoshop", "Photoshop"),
    ("STORY BOARD", "story-board", "Story Board"),
    ("DESIGN EXHIBITIONS", "design-exhibitions", "Design Exhibitions"),
    ("BRANDS", "brands", "Brands"),
    ("nivhar", "selected-work", "Selected Work"),
]


def list_images(folder):
    path = os.path.join(SRC_ROOT, folder)
    if not os.path.isdir(path):
        return []
    files = []
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if not os.path.isfile(full):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in IMG_EXTS:
            files.append(name)
    return files


def resize_copy(src, dst):
    subprocess.run(
        ["sips", "-Z", str(MAX_DIM), src, "--out", dst],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def build_section(categories, section_slug):
    out_dir = os.path.join(PROJECT_ROOT, "img", section_slug)
    os.makedirs(out_dir, exist_ok=True)
    html_parts = []
    total = 0
    for folder, slug, label in categories:
        images = list_images(folder)
        if not images:
            continue
        cat_dir = os.path.join(out_dir, slug)
        os.makedirs(cat_dir, exist_ok=True)
        item_html = []
        for idx, name in enumerate(images, start=1):
            ext = os.path.splitext(name)[1].lower()
            dest_name = f"{idx:03d}{ext}"
            src_path = os.path.join(SRC_ROOT, folder, name)
            dst_path = os.path.join(cat_dir, dest_name)
            try:
                resize_copy(src_path, dst_path)
            except subprocess.CalledProcessError:
                continue
            rel_path = f"img/{section_slug}/{slug}/{dest_name}"
            url_path = urllib.parse.quote(rel_path)
            item_html.append(
                f'<div class="work-grid__item work-grid__item--plain">'
                f'<img src="{url_path}" alt="{label}" loading="lazy">'
                f"</div>"
            )
        total += len(item_html)
        html_parts.append(
            f'<div class="gallery-category">'
            f'<h3 class="gallery-category__title">{label}</h3>'
            f'<div class="work-grid">{"".join(item_html)}</div>'
            f"</div>"
        )
        print(f"{section_slug}/{slug}: {len(item_html)} images")
    print(f"TOTAL {section_slug}: {total} images")
    return "\n".join(html_parts)


if __name__ == "__main__":
    gallery_html = build_section(GALLERY_CATEGORIES, "gallery")
    with open(os.path.join(PROJECT_ROOT, "_gallery_content.html"), "w") as f:
        f.write(gallery_html)

    design_html = build_section(DESIGN_CATEGORIES, "design-portfolio")
    with open(os.path.join(PROJECT_ROOT, "_design_content.html"), "w") as f:
        f.write(design_html)
