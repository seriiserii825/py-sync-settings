# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

py-sync-settings is a CLI tool for batch-managing git repositories across the system. It discovers all git repos under `~/`, generates repo lists, and provides interactive menus to push, pull, sync, or clone repos in bulk. It also supports GPG encryption/decryption of sensitive files (via `.gpgrc` files in repos) and git submodule handling.

## Running

```bash
uv run python main.py              # interactive menu
uv run python main.py <message>    # passes commit message to push flow
```

## Linting / Type Checking

```bash
uv run flake8 .
uv run mypy .
uv run autopep8 --in-place --recursive .
```

## Architecture

**Entry point:** `main.py` — presents a Rich table menu with 5 options: Push, Pull, Sync, Clone, Remove sync files.

**modules/** — core git operations, each file exports a single function:
- `gitPush` / `gitPull` — single-repo push/pull with `.gpgrc` encryption support and `.gitmodules` submodule handling
- `gitPushAll` / `gitPullAll` — iterate over repo list files (`~/Documents/push-repos.txt` / `pull-repos.txt`) and push/pull each
- `syncGit` — sub-menu for bulk operations: push all, pull all, or view today's commits
- `gitClone` — clones from clipboard URL (uses `xclip`)
- `checkIfPushNeeded` — uses GitPython to check dirty state
- `checkIfPullNeeded` — compares local vs remote HEAD after `git fetch`
- `getCommits` — shows today's commits across all repos, with fzf selection to copy to clipboard

**classes/** — data handling:
- `CsvHandler` — reads `exclude-dirs.csv` and `exclude-for-pull.csv` (directories to skip when scanning for repos)
- `ReposFiles` — discovers all `.git` dirs under `~/` (up to depth 8), filters by exclude lists, writes results to `~/Documents/push-repos.txt` and `~/Documents/pull-repos.txt`

**utils/** — GPG encryption helpers:
- `encryptFiles` / `decryptFiles` — encrypt/decrypt files listed in a repo's `.gpgrc` file using GPG

**libs/** — reusable UI and file utilities (Rich tables, fzf selection, file operations)

## Key Conventions

- Commit types: `feat`, `upd`, `bug-fix`, `fix`, `core` — selected via interactive menu in `utils/tableMenu.py`
- Commits are formatted as `<type>: <message>` (e.g., `feat: add new feature`)
- Uses `rich` for all terminal output (tables, panels, colored text)
- Uses `pyfzf` for fuzzy selection
- CSV exclude files use one entry per line (not comma-separated despite `.csv` extension)
- Repo list files are plain text with one repo path per line, stored in `~/Documents/`
- External tools required: `git`, `gpg`, `xclip`, `fzf`
