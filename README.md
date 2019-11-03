# getenv
#### *Keep track of your .env files*

[![asciicast](https://asciinema.org/a/267709.svg)](https://asciinema.org/a/267709)  
  
Copies your .env files from a *source dir* you provide to the *current
working dir*. You can also copy all the .env files in your working
directory to the source directory.

If you work on different clients this is a handy tool which let you
get your env files from a separate synced location.


## Requires
Linux / Mac  
Python > 3.6  

## Installation
#### Linux distro with snap support

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-white.svg)](https://snapcraft.io/getenv)
```
snap install getenv
```


#### No snap support / Or on Windows/MAC / (Or need access outside $home)
```
$ git clone https://github.com/izznogooood/getenv.git
$ cd getenv
$ python setup.py install
```

## Basic Usage
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

## Help content
```
usage: getenv.py [-h] [-v] [-c] [-l] [-f] [-o <project_name>]
                 [-s <source_dir>] [-r "Request / feedback in quotes"]

Copies .env files from "<source_dir>/<project=current_dir_name>" to current
dir.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version.
  -c, --copy            Copy .env to <source_dir>/<project=current_dir_name>
  -l, --list            List .env files in
                        <source_dir>/<project=current_dir_name>
  -f, --force           Overwrite current .env if found
  -o <project_name>, --override <project_name>
                        Override <project=current_dir_name>.
  -s <source_dir>, --source <source_dir>
                        Permanantly change source dir.
  -r "Request / feedback in quotes", --request "Request / feedback in quotes"
                        Send feedback or a request directly to the developer

```

## Config file

`~/.config/getenv.ini`

## Changelog

### [0.2.0] - 2019-06-21
 Added --list (List .env files in <source_dir>/<project=current_dir_name>)  
 Added --Version  
 Added warning if destination env is newer than source env.
