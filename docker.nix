let
  pkgs = import <nixpkgs> { };
  app = pkgs.poetry2nix.mkPoetryApplication { projectDir = ./.; };
in pkgs.dockerTools.streamLayeredImage {
  name = "personal-bot";
  tag = "latest";
  created = "now";
  contents = [ app.dependencyEnv ];
  config.Cmd = [ "runbot" ];
}
