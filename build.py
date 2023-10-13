from typing import Any, Dict, Final, List, NamedTuple, Optional, Tuple

import os

from pathlib import Path

import shutil

import glob

import json

import datetime

from jinja2 import Environment, Template, FileSystemLoader, select_autoescape

import pandoc

# Pre-defined site names
BUILD_DIR: Final[Path] = Path("site")
SRC_DIR: Final[Path] = Path("src")
STATIC_DIR: Final[Path] = Path("static")
POSTS_DIR: Final[Path] = Path("posts")
PROJS_DIR: Final[Path] = Path("projects")
TEMPLATE_DIR: Final[Path] = Path("templates")
POST_BUILD_DIR: Final[Path] = BUILD_DIR.joinpath(Path("posts"))


def make_build_dir(build_dir: Path = BUILD_DIR) -> None:
    if build_dir.exists() and build_dir.is_dir():
        return
    elif build_dir.exists() and not build_dir.is_dir():
        os.remove(build_dir)
    os.mkdir(build_dir) 


def load_templates(template_dir: Path = TEMPLATE_DIR) -> Environment:
    TemplatesBase: Environment = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape()
    )
    return TemplatesBase

HeaderTemp: Template = load_templates().get_template("header.html.jinja")
NavbarTemp: Template = load_templates().get_template("navbar.html.jinja")


def build_pages() -> None:
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
        f"{str(page_path.stem)[:-5].capitalize()} - Alia Lescoulie"

        page_header: str = header.render(title=page_title)

        page_text: str = page_temp.render(header=page_header, navbar=navbar.render())

        with open(BUILD_DIR.joinpath(page_path.stem), 'w', encoding='utf-8') as file:
            file.write(page_text) 
    

def copy_static() -> None:
    make_build_dir()
    shutil.copytree(STATIC_DIR, Path(BUILD_DIR, "static"))


class PostData(NamedTuple):
    path: Path
    directory: Path
    format: str
    static: Optional[Path]
    title: str
    authors: List[str]
    date: "date"
    description: str
    thumbnail: Path
    project: List[str]
    tags: List[str]


def parse_post(post_json: Path) -> PostData:
    with open(post_json, 'r') as file:
        post_json: Dict[str, Any] = json.load(file)

        Post: PostData = PostData(
            Path(post_json["file_path"]),
            Path(post_json["post_dir"]),
            post_json["format"],
            Path(post_json["static_dir"]),
            post_json["title"],
            post_json["authors"],
            datetime.date(
                day=post_json["day"],
                month=post_json["month"],
                year=post_json["year"]
            ),
            post_json["description"],
            Path(post_json["thumbnail"]),
            post_json["project"],
            post_json["tags"]
        )
        
    return Post
            

def collect_posts(posts_src_dir: Path = POSTS_DIR,
                  verbose: bool = False) -> List:
    post_list: List(str) = glob.glob("*/post.json", root_dir=posts_src_dir)
    if verbose:
        print(f"Collecting Posts in {posts_src_dir}")
        for post in post_list:
            print(post)
    return [parse_post(Path.joinpath(posts_src_dir, Path(json_path))) for json_path in post_list]


class PostHTML(NamedTuple):
    post_data: PostData
    post_src: str


def build_post_html(post_data: PostData,
                    post_dir: Path,
                    verbose: bool = False) -> PostHTML:
    if verbose:
        print(f"Building {post_data.path} html")
    with open(post_dir.joinpath(post_data.directory, post_data.path), 'r') as post_file:
        post_text: str = post_file.read()
        post_info: Any = pandoc.read(post_text, format=post_data.format)
        post_html: str = pandoc.write(post_info, format='html')
    return PostHTML(post_data, post_html)


def render_authors_string(author_list: List[str]) -> str:
    if len(author_list) == 0:
        raise ValueError("No authors provided")
    elif len(author_list) == 1:
        return author_list[0]
    elif len(author_list) < 1:
        return " ".join([f"{name}, " for name in author_list[:-1]]) + f"and {author_list[-1]}"


def render_date_string(date) -> str: # put a datetime date as the argument
    return date.strftime("%B %-d, %Y")


class PostBuildData(NamedTuple):
    path: Path
    directory: Path
    data: PostData 


def build_post_page(
        Post: PostHTML,
        post_build_dir: Path = POST_BUILD_DIR,
        header: Template = HeaderTemp,
        navbar: Template = NavbarTemp,
        template_name: str = "post_temp.html.jinja",
        verbose: bool = False
        ) -> PostBuildData:
    
    TemplatesBase: Environment = load_templates()

    if verbose:
        print(f"Loading template {template_name}")

    PostTemp: Template = TemplatesBase.get_template(template_name)

    header_text: str = header.render(title=f"{Post.post_data.title} - Alia Lescoulie")

    post_text: str = PostTemp.render(
        header=header_text,
        navbar=navbar.render(),
        post_title=Post.post_data.title,
        post_author=render_authors_string(Post.post_data.authors),
        post_date=render_date_string(Post.post_data.date),
        post_html=Post.post_src
        )

    post_dir: Path = post_build_dir.joinpath(Post.post_data.directory)
    post_path: Path = post_dir.joinpath(Post.post_data.path.stem + ".html")    

    if verbose:
        print(f"writing post to {post_path}")

    post_dir.mkdir(parents=True, exist_ok=True)

    with open(post_path, "w") as post_file:
        post_file.write(post_text)

    return PostBuildData(post_path, post_dir, Post.post_data)


def copy_post_files(post: PostBuildData, verbose: bool = False) -> None:
    if post.data.static is None:
        return None
    else:
        new_static_dir: Path = post.directory.joinpath("static")

        if verbose:
            print(f"Copying {post.data.static} to {new_static_dir}")

        if not new_static_dir.exists():
            os.mkdir(new_static_dir)

        shutil.copytree(post.data.static, new_static_dir, dirs_exist_ok=True)


def build_blog(post_src_dir: Path = POSTS_DIR,
               post_build_dir: Path = POST_BUILD_DIR,
               header: Template = HeaderTemp,
               navbar: Template = NavbarTemp,
               template_name: str = "post_temp.html.jinja",
               verbose: bool = False
               ) -> None:
    if verbose:
        print("Starting blog construction")

    posts: List[PostData] = collect_posts(
        posts_src_dir=post_src_dir,
        verbose=verbose
        )
    if verbose:
        print(f"Collected {len(posts)} posts")
    
    posts: List[PostHTML] = [build_post_html(
        post,
        post_src_dir,
        verbose=verbose) for post in posts]

    posts: List[PostBuildData] = [build_post_page(post,
                                                  post_build_dir=post_build_dir,
                                                  header=header,
                                                  navbar=navbar,
                                                  template_name=template_name,
                                                  verbose=verbose
                                                  )
                                   for post in posts]
    for post in posts:
        copy_post_files(post, verbose=verbose)


def clean():
    shutil.rmtree(BUILD_DIR)
