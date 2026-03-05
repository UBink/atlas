from pathlib import Path
from analyzer import get_imports_from_source, get_line_count

SKIP_PATTERNS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules',
                 'bin', 'include', 'lib', 'dist', 'build', '.egg-info'}

def read_gitignore(directory):
    """Read .gitignore file and return list of patterns to ignore."""
    gitignore_path = Path(directory) / '.gitignore'
    patterns = []

    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)

    return patterns

def should_ignore(item, gitignore_patterns):
    """Check if item should be ignored based on patterns."""
    item_name = item.name

    if item_name in SKIP_PATTERNS:
        return True

    for pattern in gitignore_patterns:
        pattern = pattern.rstrip('/')
        if pattern.startswith('*'):
            if item_name.endswith(pattern[1:]):
                return True
        elif pattern in str(item):
            return True

    return False

def get_structure(directory):
    """Build standard structure dict from local directory."""
    structure = {}
    root = Path(directory)
    gitignore_patterns = read_gitignore(directory)

    for item in root.rglob('*'):
        if any(part.startswith('.') for part in item.parts):
            continue
        if any(skip in item.parts for skip in SKIP_PATTERNS):
            continue
        if should_ignore(item, gitignore_patterns):
            continue

        relative = str(item.relative_to(root))

        file_data = {
            'is_dir': item.is_dir(),
            'size': item.stat().st_size if item.is_file() else 0,
            'imports': [],
            'line_count': None
        }

        if item.is_file() and item.suffix == '.py':
            try:
                source = item.read_text(encoding='utf-8', errors='ignore')
                file_data['imports'] = get_imports_from_source(source)
                file_data['line_count'] = get_line_count(source)
            except (PermissionError, OSError):
                pass

        structure[relative] = file_data

    return structure

def print_tree(structure, directory, prefix='', parent_path=''):
    """Print directory tree structure with ASCII art."""
    # Get immediate children of parent_path
    items = {}
    for path, info in structure.items():
        # Normalize separators
        norm_path = path.replace('\\', '/')
        norm_parent = parent_path.replace('\\', '/')

        if norm_parent and not norm_path.startswith(norm_parent):
            continue

        remaining = norm_path[len(norm_parent):].lstrip('/')
        if not remaining:
            continue

        first_part = remaining.split('/')[0]
        if first_part not in items:
            items[first_part] = {
                'is_dir': '/' in remaining or info['is_dir'],
                'full_path': (norm_parent + first_part).rstrip('/'),
                'imports': info.get('imports', [])
            }

    sorted_items = sorted(items.items())
    for i, (name, info) in enumerate(sorted_items):
        is_last = i == len(sorted_items) - 1
        connector = "└── " if is_last else "├── "

        file_info = structure.get(info['full_path'].replace('/', '\\') if '\\' in list(structure.keys())[0] else info['full_path'])
        line_count = file_info.get('line_count') if file_info else None
        line_str = f" ({line_count} lines)" if line_count else ""
        import_str = f" -> imports: {', '.join(info['imports'])}" if info['imports'] else ""
        display_name = f"{name}/" if info['is_dir'] else f"{name}{line_str}{import_str}"
    
        print(f"{prefix}{connector}{display_name}")

        if info['is_dir']:
            extension = "    " if is_last else "│   "
            print_tree(structure, directory, prefix + extension, info['full_path'] + '/')