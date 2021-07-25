let
  pkgs = import <nixpkgs> { };
  app = pkgs.poetry2nix.mkPoetryApplication { projectDir = ./.; };
in pkgs.dockerTools.streamLayeredImage {
  name = "personalBot";
  contents = [ app.dependencyEnv ];
  config.Cmd = [ "runbot" ];
}
