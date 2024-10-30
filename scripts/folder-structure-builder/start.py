import os
# run this file in the directory you want to create the files in

filename = "./scripts/folder-structure-builder/structure.txt"
# change this if you want to create files in a specific directory
base_path = os.getcwd()

prev_name = []
with open(filename, 'r') as file:
    for line in file:
        indent_count = len(line) - len(line.lstrip())
        level = indent_count // 4  # Assuming an indentation of 4 spaces.
        name = line.strip()
        name = name.replace('/', '')

        # Adjust the current path according to the indentation level

        prev_name = prev_name[:level] + [name]

        full_path = os.path.join(base_path, *prev_name)

        if '/' in line:
            os.makedirs(full_path, exist_ok=True)
        else:
            if not os.path.exists(full_path):
                open(full_path, 'a').close()
