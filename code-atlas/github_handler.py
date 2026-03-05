import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from collections import defaultdict
import ast
import sys

#Get low signal import names
low_signal_imports = sys.stdlib_module_names

def get_imports_from_source(source_code):
    """Extracts all top-level imports from a Python source string."""
    try:
        tree = ast.parse(source_code)
        file_imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    #Skip low signal imports
                    if alias.name.split(".")[0] not in low_signal_imports:
                        file_imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    if node.module.split('.')[0] not in low_signal_imports:
                        file_imports.add(node.module)
        return list(file_imports)
    except (SyntaxError, UnicodeDecodeError):
        return []

def count_github_file_types(structure):
    file_counts = defaultdict(int)
    
    for path, info in structure.items():
        if not info['is_dir']:
            # Get file extension
            if '.' in path:
                ext = '.' + path.rsplit('.', 1)[1]
            else:
                ext = 'no extension'
            file_counts[ext] += 1
    
    return dict(file_counts)

def print_github_summary(file_counts):
    """Print file type summary for GitHub repos."""
    if not file_counts:
        print("\n No files found in repository")
        return
    
    print("\n")
    print("FILE SUMMARY:")
    for ext, count in sorted(file_counts.items()):
        print(f"{ext}: {count}")
    print(f"\nTotal files: {sum(file_counts.values())}")


def parse_github_url(url):
    """Extract owner and repo from GitHub URL."""
    # Handle different formats
    url = url.rstrip('/').replace('.git', '')
    
    if url.startswith('http'):
        # https://github.com/user/repo/branch
        parts = url.split('/')
        owner = parts[-2]
        repo = parts[-1]
    else:
        # github.com/user/repo or user/repo
        url = url.replace('github.com/', '')
        parts = url.split('/')
        owner = parts[0]
        repo = parts[1]
    
    return owner, repo

def fetch_github_repo_structure(github_url):
    """Download GitHub repo ZIP and extract file structure."""
    owner, repo = parse_github_url(github_url)
    
    # Try common branches
    for branch in ['main', 'master', 'develop']:
        zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        response = requests.get(zip_url)
        
        if response.status_code == 200:
            return extract_structure_from_zip(response.content, f"{repo}-{branch}")
    
    raise ValueError(f"Could not access repo. Check URL or try: main/master branch")

def extract_structure_from_zip(zip_content, root_name):
    structure = {}
    gitignore_content = None
    zip_bytes = BytesIO(zip_content)
    
    with ZipFile(zip_bytes) as zip_file:
        # 1. Find .gitignore first
        for file_info in zip_file.infolist():
            if file_info.filename.endswith('.gitignore'):
                with zip_file.open(file_info) as f:
                    gitignore_content = f.read().decode('utf-8')
                break
        
        # 2. Build structure and EXTRACT IMPORTS
        for file_info in zip_file.infolist():
            parts = file_info.filename.split('/', 1)
            if len(parts) > 1:
                relative_path = parts[1]
                
                # Default info
                file_data = {
                    'is_dir': file_info.is_dir(),
                    'size': file_info.file_size,
                    'imports': [] # Added field
                }

                # If it's a Python file, parse it for imports
                if not file_info.is_dir() and relative_path.endswith('.py'):
                    with zip_file.open(file_info) as f:
                        source = f.read().decode('utf-8', errors='ignore')
                        file_data['imports'] = get_imports_from_source(source)

                structure[relative_path] = file_data

    return structure, gitignore_content

# --- MODIFIED: Tree printer to show imports ---
def print_github_tree(structure, gitignore_content, prefix='', parent_path=''):
    gitignore_patterns = parse_gitignore_content(gitignore_content)
    items = {}
    for path, info in structure.items():
        if not path.startswith(parent_path): continue
        remaining = path[len(parent_path):].lstrip('/')
        if not remaining: continue
        
        first_part = remaining.split('/')[0]
        if first_part not in items:
            items[first_part] = {
                'is_dir': '/' in remaining or info['is_dir'],
                'full_path': (parent_path + first_part).rstrip('/'),
                'imports': info.get('imports', []) # Carry imports over
            }
    
    sorted_items = sorted(items.items())
    for i, (name, info) in enumerate(sorted_items):
        is_last = i == len(sorted_items) - 1
        connector = "└── " if is_last else "├── "
        is_ignored = should_ignore_github(info['full_path'], gitignore_patterns)
        
        if is_ignored and not info['is_dir']: continue
        
        # Display logic: add imports to the file name if they exist
        import_str = f" -> imports: {', '.join(info['imports'])}" if info['imports'] else ""
        display_name = f"{name}/" if info['is_dir'] else f"{name}{import_str}"
        if is_ignored: display_name += " [ignored]"
        
        print(f"{prefix}{connector}{display_name}")
        
        if info['is_dir'] and not is_ignored:
            print_github_tree(structure, gitignore_content, prefix + ("    " if is_last else "│   "), info['full_path'] + '/')


SKIP_PATTERNS = {'.git', '__pycache__', 'venv', '.venv', 'node_modules', 
                 'bin', 'include', 'lib', 'dist', 'build', '.egg-info'}

def parse_gitignore_content(content):
    """Parse gitignore content into patterns list."""
    if not content:
        return []
    
    patterns = []
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            patterns.append(line)
    return patterns

def should_ignore_github(path, gitignore_patterns):
    """Check if path should be ignored based on patterns."""
    # Check hardcoded patterns
    for pattern in SKIP_PATTERNS:
        if pattern in path:
            return True
    
    # Check if starts with dot
    path_parts = path.split('/')
    for part in path_parts:
        if part.startswith('.'):
            return True
    
    # Check gitignore patterns
    for pattern in gitignore_patterns:
        pattern = pattern.rstrip('/')
        
        if pattern.startswith('*'):
            if path.endswith(pattern[1:]):
                return True
        elif pattern in path:
            return True
    
    return False

def get_repo_stats(structure):
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