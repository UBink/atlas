from pathlib import Path
from analyzer import get_repo_stats, count_file_types, print_summary, print_repo_summary
from local_handler import get_structure as get_local_structure, print_tree as print_local_tree
from github_handler import fetch_github_repo_structure, print_github_tree

def is_github_url(input_str):
    """Check if input is a GitHub URL."""
    input_str = input_str.strip().lower()
    return (
        'github.com' in input_str or
        input_str.startswith('http') or
        input_str.startswith('https')
    )

def validate_input(user_input):
    """Validate user input before processing."""
    if not user_input or user_input.strip() == "":
        print("Error: Please enter a directory path or GitHub URL")
        return False

    user_input = user_input.strip()
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

    if not validate_input(user_input):
        return

    user_input = user_input.strip()

    try:
        if is_github_url(user_input):
            print(f"\nFetching GitHub repo: {user_input}\n")
            structure, gitignore_content = fetch_github_repo_structure(user_input)
            print_github_tree(structure, gitignore_content)
        else:
            print(f"\nDirectory structure for: {user_input}\n")
            structure = get_local_structure(user_input)
            print_local_tree(structure, user_input)

        # Shared analysis for both local and GitHub
        stats = get_repo_stats(structure)
        print_repo_summary(stats)
        counts = count_file_types(structure)
        print_summary(counts)

    except FileNotFoundError:
        print("Error: Directory not found")
    except PermissionError:
        print("Error: Permission denied - cannot access this directory")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("   Please report this issue at: https://github.com/UBink/atlas/issues")

if __name__ == "__main__":
    main()