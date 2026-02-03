from pathlib import Path

def print_tree(directory, prefix=''):
    for item in Path(directory).iterdir():
        if item.name.startswith('.') or item.name == "bin" or item.name == "include" or item.name == "lib":
            continue
        print(f"{prefix}{item.name}")
        if item.is_dir():
            print_tree(item, prefix + "  ")


dir = input("Enter directory path:")

print_tree(dir)