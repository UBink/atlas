# Atlas

A lightweight tool to quickly understand code repository structure.

## Overview

Atlas helps developers explore unfamiliar codebases by providing a clear, visual representation of the project structure with intelligent filtering and file type analysis.

## Features

- Clean ASCII tree visualization of directory structure
- Respects `.gitignore` and filters common build/dependency folders
- File type recognition and statistics
- Clear distinction between files and folders (folders marked with `/`)
- Ignored folders labeled with `[ignored]` tag
- Fast and lightweight - no dependencies required

## Installation

```bash
git clone https://github.com/UBink/atlas.git
cd atlas
python atlas.py
```

## Usage

```bash
python atlas.py
```

Enter a directory path when prompted. Atlas will analyze the structure and display:
- Visual tree diagram with folders clearly marked with `/`
- Ignored folders (like `venv/`, `node_modules/`) labeled `[ignored]` but not expanded
- File type summary with counts

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
- Any patterns in your `.gitignore` file

Ignored folders are shown with an `[ignored]` tag but their contents are not displayed.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features

## Current Version

**v0.0.5** - Clear folder vs file distinction

## License

MIT