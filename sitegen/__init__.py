from pathlib import Path
import shutil

from . import build


def build_test():
    test_build_dir: Path = Path("tests/site")
    test_src_dir: Path = Path("tests/src")

    if test_build_dir.exists():
        shutil.rmtree("tests/site")
    build.make_build_dir(test_build_dir)
    
    build.copy_static(Path("site_src/static"), test_build_dir)
    build.build_pages(
        build_dir=test_build_dir,
        src_dir=test_src_dir,
    )

    blog_posts: List[build.PostBuildData] = build.build_blog(
        post_src_dir=Path("tests/test_posts"),
        post_build_dir=Path("posts"),
        site_build_dir=test_build_dir,
        verbose=True
    )

    build.build_projects(
        posts=blog_posts,
        projects_src_dir=Path("tests/test_projects"),
        site_src_dir=test_src_dir,
        site_build_dir=test_build_dir,
        posts_build_dir=Path("posts"),
        projects_build_dir=Path("projects"),
        verbose=True
    )


def build_production(): 
    build.clean()
    
    build.copy_static()
    build.build_pages()
    blog_posts: List[build.PostBuildData] = build.build_blog()
    build.build_projects(blog_posts)

