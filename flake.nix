{
  description = "My personal website";

  inputs = {
    naersk.url = "github:nix-community/naersk/master";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs@{ self, naersk, nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachSystem [ 
    "x86_64-linux"
    "aarch64-linux"
    "aarch64-darwin"
  ] (system: let
        pkgs = import nixpkgs { inherit system; };
        naersk-lib = pkgs.callPackage naersk { };
      in
      {
        defaultPackage = naersk-lib.buildPackage ./.;
        devShell = with pkgs; mkShell {
          buildInputs = [ cargo rustc rustfmt pre-commit rustPackages.clippy pandoc ];
          RUST_SRC_PATH = rustPlatform.rustLibSrc;
        };
      });}
