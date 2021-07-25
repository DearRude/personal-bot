let
  pkgs = import <nixpkgs> { };
  app = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    editablePackageSources.predictable = ./.;
  };
in pkgs.mkShell { buildInputs = [ app pkgs.poetry ]; }
