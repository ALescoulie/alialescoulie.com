from typing import Final

import os

from pathlib import Path

import glob

from jinja2 import Environment, Template, FileSystemLoader, select_autoescape


# Pre-defined site names
BUILD_DIR: Final[Path] = Path("Site")


def make_build_dir() -> None:
    if BUILD_DIR.exists() and BUILD_DIR.is_dir():
        return
    elif BUILD_DIR.exists() and not BUILD_DIR.is_dir():
        os.remove(BUILD_DIR)
    os.mkdir(BUILD_DIR) 
    return


def build_pages() -> int:
    make_build_dir() # Ensures that build_dir exists
    TemplatesBase: Environment = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape()
    )

    Pages: Environment = Environment(
        loader=FileSystemLoader("src"),
    )


    header: Template = TemplatesBase.get_template("header.html.jinja")
    navbar: Template = TemplatesBase.get_template("navbar.html.jinja")


    for page in glob.glob("src/*.html.jinja"):
        page_path: Path = Path(page)

        page_temp: Template = Pages.get_template(page_path.stem + page_path.suffix)

        page_title: str = "Alia Lescoulie" if page_path.stem == "index.html" else \
        f"{str(page_path.stem)[:-5].capitalize()} - Alia Lesoculie"

        page_header: str = header.render(title=page_title)

        page_text: str = page_temp.render(header=page_header, navbar=navbar.render())

        with open(BUILD_DIR.joinpath(page_path.stem), 'w', encoding='utf-8') as file:
            file.write(page_text)
        
    

def build_blog() -> int:
    pass


def build_full() -> int:
    

    build_pages()

    build_blog()




    return 0


def clean():
    pass


if __name__ == "__main__":
    build_pages()
