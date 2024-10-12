set shell := ["nu", "-c"]

# 枚举配方
@default: ls
  echo " "
  just --list

[group('dev')]
check:
  ruff check; nix flake check --impure --show-trace

[group('dev')]
dev:
  nix develop --impure --show-trace -c nu

[group('main')]
run:
  sage main.py

[group('dev')]
fmt:
  ruff format; nix fmt --impure

[group('cfg')]
self:
  ^$env.EDITOR justfile

[group('cfg')]
flake:
  ^$env.EDITOR flake.nix

[group('prj')]
@ls:
  ls -afm
  echo " "
  git --version
  git status
