from pathlib import Path
import shutil

import build


def main():
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

    build.build_blog(
        post_src_dir=Path("tests/test_posts"),
        post_build_dir=Path("posts"),
        site_build_dir=test_build_dir,
        templates_dir=test_templates,
        tags_dir=test_tags_dir,
        verbose=True
        )


if __name__ == "__main__":
    main()

