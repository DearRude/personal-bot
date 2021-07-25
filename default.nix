{ pkgs ? import <nixpkgs> { } }:

pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  overrides = pkgs.poetry2nix.overrides.withDefaults
    (self: super: { foo = pkgs.foo.overridePythonAttrs (oldAttrs: { }); });
}
