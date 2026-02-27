from pathlib import Path
from collections import defaultdict

SKIP_PATTERNS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules',
                 'bin', 'include', 'lib', 'dist', 'build'}

def count_file_types(directory):
    """Count files by extension."""
    file_counts = defaultdict(int)
    
    for item in Path(directory).rglob('*'):
        # Skip ignored directories
        if any(skip in item.parts for skip in SKIP_PATTERNS):
            continue
        if item.name.startswith('.'):
            continue
            
        if item.is_file():
            extension = item.suffix if item.suffix else 'no extension'
            file_counts[extension] += 1
    
    return dict(file_counts)

def print_summary(file_counts):
    """Print file type summary."""
    print("File Summary:")
    for ext, count in sorted(file_counts.items()):
        print(f"{ext}: {count}")
    print(f"\nTotal files: {sum(file_counts.values())}")