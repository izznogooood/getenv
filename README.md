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
Copied .env
Copied test.env

You're env files are stored in: /home/user/Nextcloud/Development/env/project
```

Then when your are on a new client:

```
$ getenv
Enter full path to env source dir: /home/user/Nextcloud/Development/env
"/home/user/Nextcloud/Development/env" configured as source for .env files.
Copied dev.env
Copied .env
Copied test.env

You're all set!
```
### Config file

`~/.config/getenv.ini`
