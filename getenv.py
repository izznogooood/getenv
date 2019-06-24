import argparse
import configparser
import os
import re
import sys
import getpass
from shutil import copy2 as copy
from colorama import init
from termcolor import colored

VERSION = '0.2.0'

init()
config = configparser.ConfigParser()
CONFIG_FILE_PATH = os.path.join(
    os.path.expanduser('~'), '.config', 'getenv.ini'
)
args = None


def main():
    """Main Program"""
    try:
        check_os()
        parse_args()

        # If --version is passed
        if args.version:
            print(f'getenv {VERSION}')
            sys.exit(0)

        create_update_check_config()

        # todo: If --source is passed <-- dealt with in: create_update_check_config()
        if args.source:
            sys.exit(0)

        # Load config/paths
        config.read(CONFIG_FILE_PATH)
        source_dir = config['SETTINGS']['source']
        project_name = args.override if args.override else os.path.basename(os.getcwd())

        # if --copy is passed
        if args.copy:
            local_env_files = find_env_files(os.getcwd())
            if not local_env_files:
                print('No .env files found!')
                sys.exit(1)
            else:
                copy_files_to_source(local_env_files, project_name, source_dir)

        source_env_files = find_env_files(os.path.join(source_dir, project_name))

        # If no .env files are found in source/<project_name>
        if not source_env_files:
            print('You have no env files stored for this project, did you mean to copy? [getenv -c]')
            sys.exit(1)

        # if --list is passed
        if args.list:
            print(f'Environment files stored for {project_name}:')

            for env in source_env_files:
                print(colored(env, 'yellow'))
            sys.exit(0)

        copy_files(os.path.join(source_dir, project_name), os.getcwd(), source_env_files)
        print()
        print("You're all set!")

    except KeyboardInterrupt:
        print()
        sys.exit(1)


def check_os():
    if sys.platform not in ('linux', 'darwin'):
        raise OSError(colored('This program currently only supports Unix based systems!', 'red'))


def parse_args():
    """initialize CLI arguments"""
    global args

    parser = argparse.ArgumentParser(
        description='Copies .env files from "<source_dir>/<project=current_dir_name>" to current dir.'
    )
    parser.add_argument('-v', '--version', help='Print version.', action='store_true')
    parser.add_argument(
        '-c', '--copy', help='Copy .env to <source_dir>/<project=current_dir_name>', action='store_true'
    )
    parser.add_argument(
        '-l', '--list', help='List .env files in <source_dir>/<project=current_dir_name>', action='store_true'
    )
    parser.add_argument('-f', '--force', help='Overwrite current .env if found', action='store_true')
    parser.add_argument(
        '-o', '--override', metavar='<project_name>', help='Override <project=current_dir_name>.'
    )
    parser.add_argument('-s', '--source', metavar='<source_dir>', help='Permanantly change source dir.')
    args = parser.parse_args()


def create_config(source_dir):
    config['SETTINGS'] = {
        'source': source_dir
    }
    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.config')):
        os.mkdir(os.path.join(os.path.expanduser('~'), '.config'))
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        config.write(config_file)
    print(colored(f'"{source_dir}" configured as source for .env files.', 'green'))


def create_update_check_config():
    if not os.path.exists(CONFIG_FILE_PATH) or args.source:
        if args.source:
            if os.path.exists(args.source):
                source_dir = args.source
            else:
                print(colored('Please provide a valid source dir.', 'red'))
                source_dir = None
        else:
            source_dir = None

        while not source_dir:
            source_dir = input('Enter full path to env source dir: ')
            if getpass.getuser() == 'root':
                source_dir = re.sub('~', '/root', source_dir)
            elif sys.platform == 'linux':
                source_dir = re.sub('~', f'/home/{getpass.getuser()}', source_dir)
            elif sys.platform == 'darwin':
                source_dir = re.sub('~', f'/Users/{getpass.getuser()}', source_dir)

            if not os.path.exists(source_dir):
                print(colored('Please provide a valid source dir.', 'red'))
                source_dir = None

        create_config(source_dir)


def find_env_files(path):
    try:
        _files = [
            item
            for item in os.listdir(path)
            if os.path.isfile(os.path.join(path, item))
            if os.path.splitext(item)[1] == '.env' or os.path.splitext(item)[0] == '.env'
        ]
    except FileNotFoundError:
        return None
    except PermissionError as e:
        print(colored(f'{e}', 'red'))
        return None

    return _files


def is_older_than(source, dest):
    if os.path.exists(source) and os.path.exists(dest):
        if os.path.getmtime(source) < os.path.getmtime(dest):
            answer = None
            while answer not in ('y', 'n'):
                answer = input(
                    colored(f'Warning: {source} is older than {dest}, replace? (Y/N): ', 'yellow')
                ).lstrip().rstrip().lower()
                if answer == 'n':
                    return False
                elif answer == 'y':
                    return True

    return True


def copy_files(source, dest, files):
    for file in files:
        try:
            file_source_path = os.path.join(source, file)
            file_dest_path = os.path.join(dest, file)
            result = is_older_than(file_source_path, file_dest_path)

            if os.path.exists(file_dest_path) and not result and not args.force:
                continue

            elif os.path.exists(file_dest_path) and result and not args.force:
                copy(file_source_path, file_dest_path)
                print(colored(f'Copied {file}', 'green'))

            elif args.force:
                copy(file_source_path, file_dest_path)
                print(colored(f'Copied {file}', 'green'))

            else:
                copy(file_source_path, file_dest_path)
                print(colored(f'Copied {file}', 'green'))

        except PermissionError:
            print(colored(f'You dont have permission to write to: {file_dest_path}', 'red'))
            sys.exit(1)


def copy_files_to_source(files, project_name, source_dir):
    try:
        if not os.path.exists(os.path.join(source_dir, project_name)):
            os.mkdir(os.path.join(source_dir, project_name))
    except PermissionError:
        print(colored(f'You dont have permission to write to: {os.path.join(source_dir, project_name)}', 'red'))
        sys.exit(1)

    dest_dir = os.path.join(source_dir, project_name)

    copy_files(os.getcwd(), dest_dir, files)
    print()
    print(f"You're env files are stored in: {os.path.join(source_dir, project_name)}")

    sys.exit(0)


if __name__ == "__main__":
    main()
