# atlas

A lightweight tool to quickly understand code repository structure locally or from GitHub.

## Overview

Atlas helps developers explore unfamiliar codebases by providing a clear, visual representation of the project structure with intelligent filtering and file type analysis. Analyze local projects or any public GitHub repository instantly.

## Features

- Clean ASCII tree visualization of directory structure
- **GitHub URL support** : analyze any public repo without cloning
- Respects `.gitignore` and filters common build/dependency folders
- File type recognition and statistics
- Clear distinction between files and folders (folders marked with `/`)
- Ignored folders labeled with `[ignored]` tag
- **Secure** : GitHub repos are processed in memory only, nothing touches disk
- Fast and lightweight : minimal dependencies

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

Atlas will automatically detect whether you've entered a local path or GitHub URL and analyze accordingly.

**Security Note:** When analyzing GitHub repositories, Atlas downloads the repo structure to memory only - no files are written to disk. The analysis is read-only and safe.

## Example Output

```
my-project/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── __pycache__/ [ignored]
├── tests/
│   └── test_main.py
├── venv/ [ignored]
├── node_modules/ [ignored]
├── README.md
└── package.json

========================================
File Summary:
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
- Any patterns in the repository's `.gitignore` file

Ignored folders are shown with an `[ignored]` tag but their contents are not displayed.

## Supported GitHub URL Formats

- `https://github.com/user/repo`
- `github.com/user/repo`
- `http://github.com/user/repo`

Atlas automatically detects the default branch (main, master, or develop).

## Use Cases

- **Explore unfamiliar repos** - Quickly understand project structure before diving in
- **Onboarding** - Help new team members understand codebase organization
- **Code reviews** - Get a bird's-eye view of changes and structure
- **Research** - Analyze multiple repos to compare architectures
- **Learning** - Study how popular projects are organized

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features

## Current Version

**v0.0.6** GitHub repository URL support

## Contributing

This is an early-stage project. Feedback and contributions welcome! If you find Atlas useful, please star the repo.

## License

MIT