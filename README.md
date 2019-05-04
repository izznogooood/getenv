# getenv
Keep track of your .env files

### Requires
Linux  
Python 3.6

### Usage
```
usage: python getenv.py [-h] [-c] [-o <project_name>] [-s <source_dir>]

Copies .env files from "<source_dir>/<current_dir_name>" to current dir.

optional arguments:
  -h, --help            show this help message and exit
  -c, --copy            Copy .env to <source_dir>/<current_dir_name>
  -o <project_name>, --override <project_name>
                        Override <current_dir_name>.
  -s <source_dir>, --source <source_dir>
                        Permanantly change source dir
```
### Config file

`~/.config/getenv.ini`