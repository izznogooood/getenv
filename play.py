import os


def find_env_files():
    _files = [
        item

        for item in os.listdir(os.getcwd())
        if os.path.isfile(item)
        if os.path.splitext(item)[1] == '.env' or os.path.splitext(item)[0] == '.env'
    ]
    if not _files:
        print('No .env files found!')
        exit(1)
    return _files


files = find_env_files()
if files:
    for file in files:
        print(file)