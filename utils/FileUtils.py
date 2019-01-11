def saveFile(fileName, data):
    with open(fileName, 'w') as file:
        file.write(data)


def saveBinary(fileName, data):
    with open(fileName, 'wb') as file:
        file.write(data)
    return file.name
