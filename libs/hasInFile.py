def hasInFile(filePath, word):
    with open(filePath, "r") as file:
        for line in file:
            if word in line:
                return True
    return False
