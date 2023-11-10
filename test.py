from pathlib import Path
import shutil

import build


if __name__ == "__main__":
    test_build_dir: Path = Path("tests/site")
    test_templates: Path = Path("tests/templates")
    test_src_dir: Path = Path("tests/src")

    if test_build_dir.exists():
        shutil.rmtree("tests/site")
    build.make_build_dir(test_build_dir)

    build.build_pages(
        build_dir=test_build_dir,
        templates_dir=test_templates,
        src_dir=test_src_dir,
    )

    build.copy_static(build_dir=test_build_dir)

    build.build_blog(
        post_src_dir=Path("tests/test_posts"),
        post_build_dir=Path("tests/site/posts"),
        site_build_dir=test_build_dir,
        verbose=True
        )
