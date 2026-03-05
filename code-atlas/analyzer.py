from pathlib import Path
from collections import defaultdict
import ast
import sys

low_signal_imports = sys.stdlib_module_names

def get_imports_from_source(source_code):
    """Extracts all top-level imports from a Python source string."""
    try:
        tree = ast.parse(source_code)
        file_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] not in low_signal_imports:
                        file_imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    if node.module.split('.')[0] not in low_signal_imports:
                        file_imports.add(node.module)
        return list(file_imports)
    except (SyntaxError, UnicodeDecodeError):
        return []

def get_repo_stats(structure):
    """Analyze structure dict and return repo-level stats."""
    internal_names = {Path(path).stem for path in structure if path.endswith('.py')}
    external_deps = set()
    internal_links = set()

    for path, info in structure.items():
        for imp in info.get('imports', []):
            root = imp.split('.')[0]
            if root in internal_names:
                internal_links.add(imp)
            else:
                external_deps.add(imp)

    return {
        "total_files": len([f for f in structure if not structure[f]['is_dir']]),
        "python_files": len(internal_names),
        "external": sorted(list(external_deps)),
        "internal": sorted(list(internal_links))
    }

def count_file_types(structure):
    file_counts = defaultdict(int)

    for path, info in structure.items():
        if not info['is_dir']:
            name = Path(path).name
            if name.startswith('.'):  # skip hidden files like .gitignore
                continue
            ext = Path(path).suffix or 'no extension'
            file_counts[ext] += 1

    return dict(file_counts)

def print_summary(file_counts):
    """Print file type summary."""
    if not file_counts:
        print("\nNo files found")
        return

    print("\nFILE SUMMARY:")
    for ext, count in sorted(file_counts.items()):
        print(f"{ext}: {count}")
    print(f"\nTotal files: {sum(file_counts.values())}")

def print_repo_summary(stats):
    """Print repo-level summary."""
    print("\nREPO SUMMARY")
    print(f"Total Files: {stats['total_files']} ({stats['python_files']} Python)")
    if stats['external']:
        print(f"External Dependencies: {', '.join(stats['external'])}")
    if stats['internal']:
        print(f"Internal Links: {', '.join(stats['internal'])}")