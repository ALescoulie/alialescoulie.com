from pathlib import Path
import shutil

import click

from sitegen import build_test, build_production


@click.command()
@click.option(
    "--test",
    default=False,
    help="builds the test version of the site"
    )
def build_site(test: bool):
    if test:
        build_test()
    else:
        build_production()


if __name__ == "__main__":
    build_site()

