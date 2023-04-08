# HTB
Hosting Toolbox - a small CLI for managing CT8 domains.

# Installation
The recommended way of installing is through the pipx:
```bash
pipx install git+https://github.com/jkazimierczak/htb.git
```
> Installing with `pip` is also possible, but may lead to dependency collision
> with other globally-installed packages.

# Commands
Toolbox commands can be listed with `htb --help`:
```bash
$ htb --help
Usage: htb [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  domain  Domain management tools.
```
> Note that the above output was produced using v0.1.2 and may not reflect 
> the current state of toolbox help.