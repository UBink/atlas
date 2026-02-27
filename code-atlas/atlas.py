from file_printer import print_tree
from file_counter import count_file_types, print_summary
from pathlib import Path
from github_handler import (
    fetch_github_repo_structure, 
    print_github_tree,
    count_github_file_types,
    print_github_summary,
    get_repo_stats
)

def is_github_url(input_str):
    """Check if input is a GitHub URL."""
    input_str = input_str.strip().lower()
    
    # Explicit GitHub URL patterns
    return (
        'github.com' in input_str or
        input_str.startswith('http') or
        input_str.startswith('https')
    )

def validate_input(user_input):
    """Validate user input before processing."""
    # Check for empty input
    if not user_input or user_input.strip() == "":
        print("Error: Please enter a directory path or GitHub URL")
        return False
    
    user_input = user_input.strip()
    
    # If it's a local path, check if it exists
    if not is_github_url(user_input):
        path = Path(user_input)
        if not path.exists():
            print(f"Error: Directory '{user_input}' does not exist")
            return False
        if not path.is_dir():
            print(f"Error: '{user_input}' is not a directory")
            return False
    
    return True

def main():
    user_input = input("Enter directory path or GitHub URL: ")
    
    # Validate input
    if not validate_input(user_input):
        return
    
    user_input = user_input.strip()
    
    try:
        if is_github_url(user_input):
            print(f"\nFetching GitHub repo: {user_input}\n")
            structure, gitignore_content = fetch_github_repo_structure(user_input)
            print_github_tree(structure, gitignore_content)
            stats = get_repo_stats(structure)
            print("\n")
            print(f"REPO SUMMARY")
            print(f"Total Files: {stats['total_files']} ({stats['python_files']} Python)")
            print(f"Dependencies: {', '.join(stats['unique_imports'])}")

    
    # Add file counting
            counts = count_github_file_types(structure)
            print_github_summary(counts)
            
        else:
            print(f"\nDirectory structure for: {user_input}\n")
            print_tree(user_input)
            counts = count_file_types(user_input)
            print_summary(counts)
        
    except FileNotFoundError:
        print("Error: Directory not found")
    except PermissionError:
        print("Error: Permission denied - cannot access this directory")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")
        print("   Please report this issue at: https://github.com/UBink/atlas/issues")

if __name__ == "__main__":
    main()