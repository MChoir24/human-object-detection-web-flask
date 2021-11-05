def write_csv(filename, content):
    with open(filename, 'a') as f:
        f.write(content+'\n')