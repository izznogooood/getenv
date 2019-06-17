import os

print(os.stat('./requirements.txt').st_mtime)
print(os.stat('./.env').st_mtime)
