from file_printer import print_tree
from file_counter import count_file_types, print_summary

def main():
    directory = input("Enter directory path: ")
    
    try:
        print(f"\nDirectory structure for: {directory}\n")
        print_tree(directory)
        
        counts = count_file_types(directory)
        print_summary(counts)
        
    except FileNotFoundError:
        print("Error: Directory not found!")
    except PermissionError:
        print("Error: Permission denied!")

if __name__ == "__main__":
    main()