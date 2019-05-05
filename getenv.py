import os
import configparser
import argparse
from sys import platform, exit
from shutil import copy2 as copy

config_file_path = os.path.join(
    os.path.expanduser('~'), '.config', 'getenv.ini'
    )
config = configparser.ConfigParser()
args = None


def main():
    """Main Program"""
    check_os()
    parse_args()
    check_config()
    if args.source:
        exit(0)

    config.read(config_file_path)
    source = config['SETTINGS']['source']
    project_name = args.override if args.override else os.path.basename(os.getcwd())

    if args.copy:
        copy_env_to_source(source, project_name)
        exit(0)

    if not os.path.exists(os.path.join(source, project_name, '.env')):
        print(f'No .env file for {project_name} found in: {os.path.join(source, project_name)}')
        exit(1)

    copy(os.path.join(source, project_name, '.env'), os.path.join(os.getcwd(), '.env'))


def check_os():
    if platform != 'linux':
        raise OSError('This program only runs on linux!')


def parse_args():
    """initialize CLI arguments"""
    global args

    parser = argparse.ArgumentParser(
        description='Copies .env files from "<source_dir>/<current_dir_name>" to current dir.'
    )
    parser.add_argument('-c', '--copy', help='Copy .env to <source_dir>/<current_dir_name>', action='store_true')
    parser.add_argument(
        '-o', '--override', metavar='<project_name>', help='Override <current_dir_name>.'
        )
    parser.add_argument('-s', '--source', metavar='<source_dir>', help='Permanantly change source dir.')
    args = parser.parse_args()


def create_config(source_dir):
    config['SETTINGS'] = {
        'source': source_dir
    }
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
    print(f'"{source_dir}" configered as source for .env files.')


def check_config():
    if not os.path.exists(config_file_path) or args.source:
        if args.source:
            create_config(args.source)
        else:
            source_dir = input('Enter full path to env source dir: ')
            create_config(source_dir)


def copy_env_to_source(source_dir, project_name):

    if not os.path.exists(os.path.join(source_dir, project_name)):
        os.mkdir(os.path.join(source_dir, project_name))

    if not os.path.exists(os.path.join(os.getcwd(), '.env')):
        print('No .env file found!')
        exit(1)
    copy(os.path.join(os.getcwd(), '.env'), os.path.join(source_dir, os.path.join(project_name, '.env')))


if __name__ == "__main__":
    main()
