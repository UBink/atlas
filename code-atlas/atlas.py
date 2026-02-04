from file_printer import print_tree
from file_counter import count_file_types, print_summary
from github_handler import fetch_github_repo_structure, print_github_tree

def is_github_url(input_str):
    """Check if input is a GitHub URL."""
    input_str = input_str.strip().lower()
    
    # Explicit GitHub URL patterns
    return (
        'github.com' in input_str or
        input_str.startswith('http') or
        input_str.startswith('https')
    )

def main():
    user_input = input("Enter directory path or GitHub URL: ")
    
    try:
        if is_github_url(user_input):
            print(f"\nFetching GitHub repo: {user_input}\n")
            structure = fetch_github_repo_structure(user_input)
            print_github_tree(structure)
            # TODO: Add file counting for GitHub repos later
        else:
            print(f"\nDirectory structure for: {user_input}\n")
            print_tree(user_input)
            counts = count_file_types(user_input)
            print_summary(counts)
        
    except FileNotFoundError:
        print("Error: Directory not found!")
    except PermissionError:
        print("Error: Permission denied!")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()