def appendToFile(filename, text):
    with open(filename, 'a') as file:
        file.write(text + '\n')

