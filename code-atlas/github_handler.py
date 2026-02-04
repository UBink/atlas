import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path
from collections import defaultdict

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
        print("\n⚠️  No files found in repository")
        return
    
    print("\n" + "=" * 40)
    print("File Summary:")
    print("=" * 40)
    for ext, count in sorted(file_counts.items()):
        print(f"{ext}: {count}")
    print(f"\nTotal files: {sum(file_counts.values())}")


def parse_github_url(url):
    """Extract owner and repo from GitHub URL."""
    # Handle different formats
    url = url.rstrip('/').replace('.git', '')
    
    if url.startswith('http'):
        # https://github.com/user/repo
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
    """Extract file/folder structure from ZIP bytes."""
    structure = {}
    gitignore_content = None  # Add this
    zip_bytes = BytesIO(zip_content)
    
    with ZipFile(zip_bytes) as zip_file:
        # First, find and read .gitignore
        for file_info in zip_file.infolist():
            if file_info.filename.endswith('.gitignore'):
                with zip_file.open(file_info) as f:
                    gitignore_content = f.read().decode('utf-8')
                break
        
        # Then build structure
        for file_info in zip_file.infolist():
            # Remove the root folder name from path
            parts = file_info.filename.split('/', 1)
            if len(parts) > 1:
                relative_path = parts[1]
                structure[relative_path] = {
                    'is_dir': file_info.is_dir(),
                    'size': file_info.file_size
                }
    
    return structure, gitignore_content  # Return BOTH

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

def print_github_tree(structure, gitignore_content, prefix='', parent_path=''):
    """Print GitHub repo structure in tree format with [ignored] tags."""
    gitignore_patterns = parse_gitignore_content(gitignore_content)
    
    # Group by immediate children
    items = {}
    for path, info in structure.items():
        if not path.startswith(parent_path):
            continue
        
        remaining = path[len(parent_path):].lstrip('/')
        if not remaining:
            continue
        
        first_part = remaining.split('/')[0]
        if first_part not in items:
            is_dir = '/' in remaining or info['is_dir']
            full_path = (parent_path + first_part).rstrip('/')
            
            items[first_part] = {
                'is_dir': is_dir,
                'full_path': full_path
            }
    
    sorted_items = sorted(items.items())
    
    for i, (name, info) in enumerate(sorted_items):
        is_last = i == len(sorted_items) - 1
        connector = "└── " if is_last else "├── "
        
        # Check if ignored
        is_ignored = should_ignore_github(info['full_path'], gitignore_patterns)
        
        # Format display
        if info['is_dir']:
            display_name = f"{name}/" + (" [ignored]" if is_ignored else "")
        else:
            display_name = name + (" [ignored]" if is_ignored else "")
        
        # Skip ignored files, show ignored folders
        if is_ignored and not info['is_dir']:
            continue
        
        print(f"{prefix}{connector}{display_name}")
        
        # Recurse into non-ignored directories
        if info['is_dir'] and not is_ignored:
            extension = "    " if is_last else "│   "
            print_github_tree(structure, gitignore_content, prefix + extension, info['full_path'] + '/')