def get_data_from_file(filepath):
    file = open(filepath, 'r')
    data = file.read()
    return data
