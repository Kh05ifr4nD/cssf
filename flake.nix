{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    devenv.url = "github:cachix/devenv";
    systems.url = "github:nix-systems/default";
  };
  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs =
    inputs@{
      devenv,
      flake-parts,
      nixpkgs,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devenv.flakeModule
      ];

      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          system,
          ...
        }:
        {
          # Per-system attributes can be defined here. The self' and inputs'
          # module parameters provide easy access to attributes of the same
          # system.

          # Equivalent to  inputs'.nixpkgs.legacyPackages.hello;
          packages.default = pkgs.hello;
          devenv.shells.default = {
            languages.python = {
              enable = true;
            };
            packages = with pkgs; [
              nodejs_18
              (sage.override {
                extraPythonPackages =
                  ps: with ps; [
                    loguru
                    reflex
                  ];
                requireSageTests = false;
              })
            ];
            enterShell = '''';
          };
          formatter = pkgs.nixfmt-rfc-style;
        };
      systems = import inputs.systems;
    };
}
