name: "Build and Deploy alialescoulie.com"
on:
  pull_request:
  push:
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: cachix/install-nix-action@v22
      with:
        github_access_token: ${{ secrets.GITHUB_TOKEN }}
    - name: Cloning blog posts from GitHub repo
    - run: git clone https://github.com/ALescoulie/blog_posts.git
    - name: Building Site Generator with Nix
    - run: nix build
    - name: Verifying flake
    - run: nix flake check
    - name: Building site
    - run: poetry run build

