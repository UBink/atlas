# atlas

A lightweight CLI tool to quickly understand code repository structure locally or from GitHub.

## Overview

Atlas helps developers explore unfamiliar codebases by providing a clear, visual representation of project structure with intelligent filtering, file type analysis, and dependency tracking. Analyze local projects or any public GitHub repository instantly.

## Features

- Clean ASCII tree visualization of directory structure
- **GitHub URL support**: analyze any public repo without cloning
- **Import extraction**: see what each Python file imports, inline in the tree
- **Dependency summary**: repo-level view of external vs internal dependencies
- **Low-signal filtering**: stdlib imports (os, sys, etc.) automatically hidden
- Respects `.gitignore` and filters common build/dependency folders
- File type recognition and statistics
- Clear distinction between files and folders (folders marked with `/`)
- Ignored folders labeled with `[ignored]` tag
- **Secure**: GitHub repos are processed in memory only, nothing touches disk
- Fast and lightweight: minimal dependencies

## Installation

```bash
git clone https://github.com/UBink/atlas.git
cd atlas
pip install requests  # Only dependency for GitHub URL support
python atlas.py
```

## Usage

### Analyze Local Directory
```bash
python atlas.py
# Enter: /path/to/your/project
```

### Analyze GitHub Repository
```bash
python atlas.py
# Enter: https://github.com/torvalds/linux
# Or: github.com/user/repo
```

Atlas automatically detects whether you've entered a local path or GitHub URL and analyzes accordingly.

**Security Note:** When analyzing GitHub repositories, Atlas downloads the repo structure to memory only  meaning no files are written to disk. The analysis is read-only and safe.

## Example Output

```
my-project/
├── src/
│   ├── main.py -> imports: requests, flask
│   ├── utils.py
│   └── __pycache__/ [ignored]
├── tests/
│   └── test_main.py
├── venv/ [ignored]
├── node_modules/ [ignored]
├── README.md
└── package.json

REPO SUMMARY
Total Files: 5 (3 Python)
External Dependencies: requests, flask
Internal Links: utils

========================================
FILE SUMMARY:
========================================
.json: 1
.md: 1
.py: 3

Total files: 5
```

## What Gets Filtered

Atlas automatically ignores common build artifacts and dependencies:
- Hidden files and folders (`.git`, `.venv`, etc.)
- Python: `__pycache__`, `*.pyc`, `venv/`, `.venv/`
- Node.js: `node_modules/`
- Build outputs: `dist/`, `build/`, `*.egg-info`
- Standard library imports (`os`, `sys`, `pathlib`, etc.) in dependency tracking
- Any patterns in the repository's `.gitignore` file

Ignored folders are shown with an `[ignored]` tag but their contents are not displayed.

## Supported GitHub URL Formats

- `https://github.com/user/repo`
- `github.com/user/repo`
- `http://github.com/user/repo`

Atlas automatically detects the default branch (main, master, or develop).

## Use Cases

- **Explore unfamiliar repos** — Quickly understand project structure before diving in
- **Onboarding** — Help new team members understand codebase organization
- **Dependency auditing** — See external vs internal imports at a glance
- **Code reviews** — Get a bird's-eye view of changes and structure
- **Research** — Analyze multiple repos to compare architectures
- **Learning** — Study how popular projects are organized

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features.

## Current Version

**v0.1.4** — Distinguish external vs internal imports

## Contributing

This is an early-stage project. Feedback and contributions welcome! If you find Atlas useful, please star the repo.

## License

MIT