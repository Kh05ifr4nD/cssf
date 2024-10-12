set shell := ["nu", "-c"]

@default: ls
  echo " "
  just --list

[group('dev')]
ck:
  ruff check; nix flake check --show-trace

[group('dev')]
dev:
  nix develop --show-trace -c nu

[group('cfg')]
fla:
  ^$env.EDITOR flake.nix

[group('dev')]
fmt:
  ruff format; nix fmt

[group('prj')]
@ls:
  ls -afm
  echo " "
  git --version
  git status

[group('main')]
run:
  sage main.py

[group('cfg')]
self:
  ^$env.EDITOR justfile

[group('dev')]
upd:
  nix flake update
