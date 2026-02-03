from pathlib import Path

SKIP_PATTERNS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 'bin', 'include', 'lib'}

def print_tree(directory, prefix='', is_last=True):
    items = [item for item in Path(directory).iterdir() 
             if not item.name.startswith('.') and item.name not in SKIP_PATTERNS]
    
    for i, item in enumerate(items):
        is_last_item = i == len(items) - 1
        connector = "└── " if is_last_item else "├── "
        print(f"{prefix}{connector}{item.name}")
        
        if item.is_dir():
            extension = "    " if is_last_item else "│   "
            print_tree(item, prefix + extension, is_last_item)
