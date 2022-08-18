{
  description = "Personal bot";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    flake-utils.inputs.nixpkgs.follows = "nixpkgs";
    poetry.url = "github:nix-community/poetry2nix";
    poetry.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, poetry }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry.overlay ];
        };
        inherit (pkgs) poetry2nix;
      in {
        # poetry2nix builds pillow without libraqm
        # packages.default = poetry2nix.mkPoetryApplication {
        #   projectDir = ./.;
        #   python = pkgs.python310Full;
        # };
        devShells.default = import ./shell.nix { inherit pkgs; };
      });
}
