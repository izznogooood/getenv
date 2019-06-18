import argparse
import configparser
import os
from shutil import copy2 as copy
from sys import platform, exit
from colorama import init
from termcolor import colored

VERSION = '0.2.0'

init()
config_file_path = os.path.join(
    os.path.expanduser('~'), '.config', 'getenv.ini'
)
config = configparser.ConfigParser()
args = None


def main():
    """Main Program"""
    try:
        check_os()
        parse_args()

        # If --version is passed
        if args.version:
            print(f'getenv {VERSION}')
            exit(0)

        create_update_check_config()

        # If --source is passed
        if args.source:
            exit(0)

        # Load config/paths
        config.read(config_file_path)
        source = config['SETTINGS']['source']
        project_name = args.override if args.override else os.path.basename(os.getcwd())

        # if --copy is passed
        if args.copy:
            local_env_files = find_env_files(os.getcwd())
            if not local_env_files:
                print('No .env files found!')
                exit(0)
            copy_env_to_source(local_env_files, source, project_name)
            print()
            print(f"You're env files are stored in: {os.path.join(source, project_name)}")
            exit(0)

        source_env_files = find_env_files(os.path.join(source, project_name))

        # If no .env files are found in source/<project_name>
        if not source_env_files:
            print('You have no env files stored for this project, did you mean to copy? [getenv -c]')
            exit(0)

        # if --list is passed
        if args.list:
            print(f'Environment files stored for {project_name}:')

            for env in source_env_files:
                print(colored(env, 'yellow'))
            exit(0)

        copy_env_from_source(source_env_files, source, project_name)
        print()
        print("You're all set!")

    except KeyboardInterrupt:
        print()
        exit(1)


def check_os():
    if platform not in ('linux', 'darwin'):
        raise OSError('This program currently only supports Unix based systems!')


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
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
    print(colored(f'"{source_dir}" configured as source for .env files.', 'green'))


def create_update_check_config():
    if not os.path.exists(config_file_path) or args.source:
        source_dir = None
        try:
            while not source_dir:
                source_dir = args.source if args.source else input('Enter full path to env source dir: ')
                
                expand = source_dir.split('~')
                if len(expand) > 1:
                    source_dir = os.path.expanduser('~') + expand[1]
                else:
                    source_dir = expand[0]
                
                source_dir = source_dir if os.path.exists(source_dir) else None
                if not source_dir:
                    print(colored('You have entered a non existent path, please try again.', 'red'))
        except KeyboardInterrupt:
            print()
            exit(1)
        
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


def copy_env_from_source(files, source, project_name):
    for file in files:
        file_source_path = os.path.join(source, project_name, file)
        file_dest_path = os.path.join(os.getcwd(), file)

        if os.path.exists(file_dest_path) and not args.force:
            answer = None
            while answer not in ('y', 'n'):
                answer = input(f'Overwrite {file_dest_path}? (Y/N): ').lstrip().rstrip().lower()
                if answer == 'n':
                    continue
                elif answer == 'y':
                    copy(file_source_path, file_dest_path)
                    print(colored(f'Copied {file}', 'green'))
        else:
            copy(file_source_path, file_dest_path)
            print(colored(f'Copied {file}', 'green'))


def copy_env_to_source(files, source_dir, project_name):
    try:
        if not os.path.exists(os.path.join(source_dir, project_name)):
            os.mkdir(os.path.join(source_dir, project_name))

        for file in files:
            copy(os.path.join(os.getcwd(), file), os.path.join(source_dir, project_name, file))
            print(colored(f'Copied {file}', 'green'))
    
    except PermissionError:
        print(colored(f'You dont have permission to write to: {source_dir}', 'red'))
        exit(1)


if __name__ == "__main__":
    main()
