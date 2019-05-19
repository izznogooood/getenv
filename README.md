# getenv
#### *Keep track of your .env files*

Copies your .env files from a *source dir* you provide to the *current
working dir*. You can also copy all the .env files in your working
directory to the source directory.

If you work on different clients this is a handy tool which let you 
keep your env files separate from your repositories. 


### Requires
Linux  
Python > 3.6  

### Usage
Lets say you have a Nextcloud server you trust with your .env's.  
In your project dir.:

```
$ getenv -c
Enter full path to env source dir: /home/user/Nextcloud/Development/env
"/home/user/Nextcloud/Development/env" configured as source for .env files.
Copied dev.env
Copied test.env

You're env files are stored in: /home/user/Nextcloud/Development/env/project
```

Then when your are on a new client:

```
$ getenv
Enter full path to env source dir: /home/user/Nextcloud/Development/env
"/home/user/Nextcloud/Development/env" configured as source for .env files.
Copied dev.env
Copied test.env

You're all set!
```
You will be asked for source dir one time pr new client. The next time
you run getenv:

```
$ getenv
Copied dev.env
Copied test.env

You're all set!
```

### Installation
```
$ git clone https://github.com/izznogooood/getenv.git
$ python setup.py install
```

### Help content
```
usage: getenv [-h] [-c] [-f] [-o <project_name>] [-s <source_dir>]

Copies .env files from "<source_dir>/<project=current_dir_name>" to current
dir.

optional arguments:
  -h, --help            show this help message and exit
  -c, --copy            Copy .env to <source_dir>/<project=current_dir_name>
  -f, --force           Overwrite current .env if found
  -o <project_name>, --override <project_name>
                        Override <project=current_dir_name>.
  -s <source_dir>, --source <source_dir>
                        Permanantly change source dir.
```

### Config file

`~/.config/getenv.ini`
