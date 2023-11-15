{
  description = "My personal website";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs-pandoc.url = "github:nixos/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, nixpkgs-pandoc, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        customOverrides = final: prev: {
          pandoc = prev.pandoc.overrideAttrs (oldAttrs: {
            buildInputs = [ prev.setuptools ];
            runtimeInputs = [ prev.setuptools ];
          });
        };

        pandoc = nixpkgs-pandoc.legacyPackages.${system}.pandoc;

        app = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          overrides =
            [ pkgs.poetry2nix.defaultPoetryOverrides customOverrides ];
        };

        # DON'T FORGET TO PUT YOUR PACKAGE NAME HERE, REMOVING `throw`
        packageName = "alialescoulie.com";
      in {
        packages.${packageName} = app;

        packages.default = self.packages.${system}.${packageName};

        devShells.default = pkgs.mkShell {
          buildInputs = [ pkgs.poetry pandoc ];
          inputsFrom = builtins.attrValues self.packages.${system};
        };
      });
}
