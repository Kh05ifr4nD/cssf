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
 nix fmt

[group('prj')]
init:
  #!/usr/bin/env nu
  if not (".venv" | path exists) {  
    print "正在创建虚拟环境"
    uv venv
  }
  if not ("pyproject.toml" | path exists) {
    print "正在初始化项目"
    uv init
  } 
  print "初始化已完成"

[group('prj')]
@ls:
  ls -afm
  echo " "
  git --version
  git status

[group('main')]
run:
  python main.py

[group('cfg')]
self:
  ^$env.EDITOR justfile

[group('dev')]
upd:
  nix flake update
