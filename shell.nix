{ pkgs ? import <nixpkgs> { } }:

with pkgs;

mkShell {
  buildInputs = [
    pkgs.python310Full
    pkgs.poetry
    pkgs.black
    pkgs.python310Packages.pyflakes

  ];
  shellHook = ''
    export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:${pkgs.fribidi.out}/lib/pkgconfig:${pkgs.zlib.dev}/lib/pkgconfig
  '';
}
