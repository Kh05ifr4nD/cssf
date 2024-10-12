{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
  };
  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs =
    inputs@{
      flake-parts,
      nixpkgs,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          self,
          system,
          ...
        }:
        {
          devShells.default = pkgs.mkShell {
            buildInputs = with pkgs; [
              qt6.qtbase
              qt6.full
              qtcreator
            ];
            nativeBuildInputs = with pkgs; [
              qt6.wrapQtAppsHook
            ];
            packages = with pkgs; [
              (sage.override {
                extraPythonPackages =
                  ps: with ps; [
                    loguru
                    pygobject3
                    pyside6
                    qt-material
                  ];
                requireSageTests = false;
              })
            ];
            shellHook = '''';
          };
          formatter = pkgs.nixfmt-rfc-style;
        };
      systems = import inputs.systems;
    };
}
