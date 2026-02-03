from pathlib import Path

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

def should_ignore(item, gitignore_patterns, skip_patterns):
    """Check if item should be ignored based on patterns."""
    item_name = item.name
    
    # Check hardcoded skip patterns
    if item_name in skip_patterns:
        return True
    
    # Check gitignore patterns
    for pattern in gitignore_patterns:
        pattern = pattern.rstrip('/')
        
        if pattern.startswith('*'):
            if item_name.endswith(pattern[1:]):
                return True
        elif pattern in str(item):
            return True
    
    return False

def print_tree(directory, prefix='', is_last=True, gitignore_patterns=None):
    """Print directory tree structure with ASCII art."""
    if gitignore_patterns is None:
        gitignore_patterns = read_gitignore(directory)
    
    try:
        items = list(Path(directory).iterdir())
    except PermissionError:
        return
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        connector = "└── " if is_last_item else "├── "
        
        # Check if ignored
        is_ignored = (item.name.startswith(".") or 
                      item.name in SKIP_PATTERNS or 
                      should_ignore(item, gitignore_patterns, SKIP_PATTERNS))
        
        # Skip ignored FILES completely
        if is_ignored and item.is_file():
            continue
        
        # Format name - show folders with [ignored] tag if needed
        if item.is_dir():
            display_name = f"{item.name}/" + (" [ignored]" if is_ignored else "")
        else:
            display_name = item.name
        
        print(f"{prefix}{connector}{display_name}")
        
        # Recurse into directories ONLY if not ignored
        if item.is_dir() and not is_ignored:
            extension = "    " if is_last_item else "│   "
            print_tree(item, prefix + extension, is_last_item, gitignore_patterns)