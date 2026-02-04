import requests
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path

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
    zip_bytes = BytesIO(zip_content)
    
    with ZipFile(zip_bytes) as zip_file:
        for file_info in zip_file.infolist():
            # Remove the root folder name from path
            # e.g., "repo-main/src/file.py" → "src/file.py"
            parts = file_info.filename.split('/', 1)
            if len(parts) > 1:
                relative_path = parts[1]
                structure[relative_path] = {
                    'is_dir': file_info.is_dir(),
                    'size': file_info.file_size
                }
    
    return structure

def print_github_tree(structure, prefix='', parent_path=''):
    """Print GitHub repo structure in tree format."""
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
            items[first_part] = {
                'is_dir': '/' in remaining,
                'full_path': parent_path + first_part
            }
    
    sorted_items = sorted(items.items())
    
    for i, (name, info) in enumerate(sorted_items):
        is_last = i == len(sorted_items) - 1
        connector = "└── " if is_last else "├── "
        
        display_name = name + '/' if info['is_dir'] else name
        print(f"{prefix}{connector}{display_name}")
        
        if info['is_dir']:
            extension = "    " if is_last else "│   "
            print_github_tree(structure, prefix + extension, info['full_path'] + '/')