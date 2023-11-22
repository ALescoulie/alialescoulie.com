from typing import Any, Dict, Final, List, NamedTuple, Optional, Tuple, Set

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
SRC_DIR: Final[Path] = Path("site_src")
STATIC_DIR: Final[Path] = Path("site_src/static")
POSTS_DIR: Final[Path] = Path("posts")
PROJS_DIR: Final[Path] = Path("projects")
TEMPLATE_DIR: Final[Path] = Path("sitegen/templates")
POST_BUILD_DIR: Final[Path] = BUILD_DIR.joinpath(Path("posts"))
TAGS_DIR: Final[Path] = BUILD_DIR.joinpath(Path("tags"))


def make_build_dir(build_dir: Path = BUILD_DIR) -> None:
    r"""Makes the sites build directory if it does not already exist.

    Arguments
    ---------

    build_dir: The directory name to be created

    """
    if build_dir.exists() and build_dir.is_dir():
        return
    elif build_dir.exists() and not build_dir.is_dir():
        os.remove(build_dir)
    os.mkdir(build_dir) 


def load_templates(templates_dir: Path = TEMPLATE_DIR,
                   verbose: bool = False) -> Environment:
    r"""Loads the Jinja templates from the specified directory into an
    Environment. The returned object can generate jinja templates by
    calling `get_template("template_path.html.jinja")`

    By default gets templates from the `templates` directory.
    """
    if verbose:
        print(f"Loading templates from {templates_dir}")
    TemplatesBase: Environment = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape()
    )
    return TemplatesBase


def build_pages(build_dir: Path = BUILD_DIR,
                templates_dir: Path = TEMPLATE_DIR,
                src_dir: Path = SRC_DIR) -> None:
    r"""Builds the jinja templates in the source dir into html files in the
    build dir using the header and navbar jinja templates in the provided
    templates dir.
    """
    make_build_dir(build_dir=build_dir) # Ensures that build_dir exists

    TemplatesBase: Environment = load_templates(templates_dir=templates_dir)

    Pages: Environment = Environment(
        loader=FileSystemLoader(src_dir),
    )


    header: Template = TemplatesBase.get_template("header.html.jinja")
    navbar: Template = TemplatesBase.get_template("navbar.html.jinja")


    for page in glob.glob(f"{src_dir}/*.html.jinja"):
        page_path: Path = Path(page)

        page_temp: Template = Pages.get_template(page_path.stem + page_path.suffix)

        page_title: str = "Alia Lescoulie" if page_path.stem == "index.html" else \
        f"{str(page_path.stem)[:-5].capitalize()} - Alia Lescoulie"

        page_header: str = header.render(title=page_title)

        page_text: str = page_temp.render(header=page_header, navbar=navbar.render())

        with open(build_dir.joinpath(page_path.stem), 'w', encoding='utf-8') as file:
            file.write(page_text) 
    

def copy_static(static_dir: Path = STATIC_DIR,
                build_dir: Path = BUILD_DIR) -> None:
    make_build_dir(build_dir=build_dir)
    shutil.copytree(static_dir, Path(build_dir, "static"))


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


def parse_post(post_json_path: Path, posts_dir: Path) -> PostData:
    with open(post_json_path, 'r') as file:
        post_json: Dict[str, Any] = json.load(file)

        Post: PostData = PostData(
            Path(post_json["file_path"]),
            Path(post_json["post_dir"]),
            post_json["format"],
            Path(post_json["static_dir"]) if post_json["static_dir"] is not None else None,
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
    return [
        parse_post(
            Path.joinpath(posts_src_dir, Path(json_path)),
            posts_src_dir) for json_path in post_list
            ]


class PostHTML(NamedTuple):
    post_data: PostData
    post_src: str


def build_post_html(post_data: PostData,
                    post_src_dir: Path = POSTS_DIR,
                    verbose: bool = False) -> PostHTML:
    if verbose:
        print(f"Building {post_data.path} html")

    post_src_path: Path = post_src_dir.joinpath(post_data.directory,
                                                post_data.path
                                                )
    with open(post_src_path, 'r') as post_file:
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
        site_build_dir: Path = BUILD_DIR,
        post_build_dir: Path = POST_BUILD_DIR,
        templates_dir: Path = TEMPLATE_DIR, 
        post_template_name: str = "post_temp.html.jinja",
        verbose: bool = False
        ) -> PostBuildData:
    
    TemplatesBase: Environment = load_templates(
            templates_dir,
            verbose
        )

    header: Template = TemplatesBase.get_template("header.html.jinja")
    navbar: Template = TemplatesBase.get_template("navbar.html.jinja")

    if verbose:
        print(f"Loading template {post_template_name}")

    PostTemp: Template = TemplatesBase.get_template(post_template_name)

    header_text: str = header.render(title=f"{Post.post_data.title} - Alia Lescoulie", depth="../../")

    post_text: str = PostTemp.render(
        header=header_text,
        navbar=navbar.render(depth="../../"),
        post_title=Post.post_data.title,
        post_author=render_authors_string(Post.post_data.authors),
        post_date=render_date_string(Post.post_data.date),
        post_html=Post.post_src
        )

    post_dir: Path = site_build_dir.joinpath(post_build_dir, Post.post_data.directory)
    post_path: Path = post_dir.joinpath(Post.post_data.path.stem + ".html")    

    if verbose:
        print(f"writing post to {post_path}")

    post_dir.mkdir(parents=True, exist_ok=True)

    with open(post_path, "w") as post_file:
        post_file.write(post_text)

    return PostBuildData(post_path, post_dir, Post.post_data)


def copy_post_files(post: PostBuildData,
                    site_build_dir: Path = BUILD_DIR,
                    post_src_dir: Path = POSTS_DIR,
                    post_build_dir: Path = POST_BUILD_DIR,
                    verbose: bool = False) -> None:
    if post.data.static is None:
        return None
    else:
        new_static_dir: Path = site_build_dir.joinpath(post_build_dir,
                                                       post.data.directory,
                                                       "static") 

        if verbose:
            print(f"Copying {post.data.static} to {new_static_dir}")

        if not new_static_dir.exists():
            os.mkdir(new_static_dir)

        shutil.copytree(
            post_src_dir.joinpath(post.data.directory, post.data.static),
            new_static_dir, 
            dirs_exist_ok=True
        )


def render_tags(tags: List[str], templates_dir, verbose: bool = False) -> None:
    TemplatesBase: Environment = load_templates(
        templates_dir,
        verbose
    )

    tag_temp: Template = TemplatesBase.get_template("tag.html.jinja")
    tag_list: List[str] = [
        tag_temp.render(
            link=f"{tag}.html",
            tag=tag
        ) for tag in tags
    ]

    return ', '.join(tag_list) 


def build_blog_page(posts: List[PostBuildData],
                    templates_dir: Path = TEMPLATE_DIR,
                    site_build_dir: Path = BUILD_DIR,
                    post_build_dir: Path = POST_BUILD_DIR,
                    blog_page_path: Path = Path("blog.html"),
                    verbose: bool = False) -> None:

    if verbose:
        print(f"Building blog page")

    TemplatesBase: Environment = load_templates(templates_dir, verbose)

    header: Template = TemplatesBase.get_template("header.html.jinja")
    navbar: Template = TemplatesBase.get_template("navbar.html.jinja")
    block: Template = TemplatesBase.get_template("post_block.html.jinja")

    blog_page: Template = TemplatesBase.get_template("blog.html.jinja")

    date_sort = lambda x : x.data.date

    reverse_cron_posts: List[PostBuildData] = sorted(posts,
                                                     key=date_sort,
                                                     reverse=True)
    
    if verbose:
        print("Posts sorted")

    post_blocks: List[str] = []

    for post in reverse_cron_posts:
        if verbose:
            print(f"Building block for {post.data.title}")
        post_blocks.append(
            block.render(
                title=post.data.title,
                img_link=post_build_dir.joinpath(post.data.directory,
                                                 post.data.thumbnail),
                link=post_build_dir.joinpath(post.data.directory,
                                             post.data.path.stem + ".html"),
                date=render_date_string(post.data.date),
                author=render_authors_string(post.data.authors),
                summary=post.data.description + " read more ...",
                tags=render_tags(post.data.tags, templates_dir, verbose)
            )
        )

    blog_page_text: str = blog_page.render(
        header=header.render(title="Blog"),
        navbar=navbar.render(),
        posts="\n".join(post_blocks)
    )
    
    with open(site_build_dir.joinpath(blog_page_path), 'w') as blog_file:
        if verbose:
            print(
                f"Writing page to {site_build_dir.joinpath(blog_page_path)}"
                )
        blog_file.write(blog_page_text)


def build_tags_pages(posts: List[PostBuildData],
                     templates_dir: Path = TEMPLATE_DIR,
                     site_build_dir: Path = BUILD_DIR,
                     post_build_dir: Path = POST_BUILD_DIR,
                     verbose: bool = False) -> None:
    tags_set: List[str] = []
    for post in posts:
        for tag in post.data.tags:
            tags_set.append(tag)

    tags_set: Set[str] = set(tags_set)

    if verbose:
        print(f"Found tags {tags_set}")

    tags_map: Dict[str, List[PostBuilData]] = {tag: [] for tag in tags_set}

    for post in posts:
        for tag in post.data.tags:
            tags_map[tag].append(post)

    for tag in tags_map.keys():
        build_blog_page(tags_map[tag],
                        templates_dir = templates_dir,
                        site_build_dir = site_build_dir,
                        post_build_dir = post_build_dir,
                        blog_page_path = Path(f"{tag}.html"),
                        verbose = verbose
                        )


def build_blog(post_src_dir: Path = POSTS_DIR,
               post_build_dir: Path = POST_BUILD_DIR,
               site_build_dir: Path = BUILD_DIR,
               templates_dir: Path = TEMPLATE_DIR,
               tags_dir: Path = TAGS_DIR,
               post_template_name: str = "post_temp.html.jinja",
               verbose: bool = False
               ) -> None:
    r"""Builds the blog over several steps
    """
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
        post_src_dir = post_src_dir,
        verbose=verbose) for post in posts]

    posts: List[PostBuildData] = [
            build_post_page(post,
                            site_build_dir=site_build_dir,
                            post_build_dir=post_build_dir,
                            templates_dir=templates_dir,
                            post_template_name=post_template_name,
                            verbose=verbose
                            ) for post in posts
        ]

    for post in posts:
        copy_post_files(
            post,
            site_build_dir=site_build_dir,
            post_src_dir=post_src_dir,
            post_build_dir=post_build_dir,
            verbose=verbose
        )
    
    build_blog_page(posts,
                    templates_dir,
                    site_build_dir,
                    post_build_dir,
                    verbose=verbose)

    build_tags_pages(posts,
                     templates_dir = templates_dir,
                     site_build_dir = site_build_dir,
                     post_build_dir = post_build_dir,
                     verbose = verbose)


#def build_project_page(projects_dir: Path,
#                       templates_dir: Path,
#                       site_build_dir: Path
#                       projects_build_dir: Path
#                       verbose: bool = True)
    

def clean(build_dir: Path = BUILD_DIR):
    r"""Warning will delete everything in this directory."""
    shutil.rmtree(build_dir)

