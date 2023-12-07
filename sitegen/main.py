from pathlib import Path
import shutil

import click

import build


@click.command()
@click.option("test", help="Builds a test version of the site in sitegen/tests/site")
def test_build():
    test_build_dir: Path = Path("tests/site")
    test_templates: Path = Path("templates")
    test_src_dir: Path = Path("tests/src")
    test_tags_dir: Path = Path("tags")

    if test_build_dir.exists():
        shutil.rmtree("tests/site")
    build.make_build_dir(test_build_dir)
    
    build.copy_static(Path("../site_src/static"), test_build_dir)
    build.build_pages(
        build_dir=test_build_dir,
        templates_dir=test_templates,
        src_dir=test_src_dir,
    )

    blog_posts: List[build.PostBuildData] = build.build_blog(
        post_src_dir=Path("tests/test_posts"),
        post_build_dir=Path("posts"),
        site_build_dir=test_build_dir,
        templates_dir=test_templates,
        tags_dir=test_tags_dir,
        verbose=True
    )

    build.build_projects(
        Path("tests/test_projects"),
        blog_posts,
        test_templates,
        test_src_dir,
        test_build_dir,
        Path("posts"),
        Path("projects"),
        verbose=True
    )

@click.command()
@click.option("build", help="builds site at site_out")
def build():
    
    build.clean()
    
    buid.copy_static()
    build.build_pages()
    blog_posts: List[build.PostBuildData] = build.build_blog()
    build.build_projects(blog_posts)

