from pathlib import Path
import shutil

import build


if __name__ == "__main__":
    
    build.build_blog(
        post_src_dir=Path("tests/test_posts"),
        post_build_dir=Path("tests/site/posts"),
        verbose=True
        )
