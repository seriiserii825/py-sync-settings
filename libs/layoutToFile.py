def layoutToFile(layout, filename):
    layout_file_content = '';
    with open(layout, 'r') as file:
        layout_file_content = file.read()
    with open(filename, 'w') as file:
        file.write(layout_file_content)
