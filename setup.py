from setuptools import setup


# noinspection PyBroadException
def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except:
        return ''


setup(
    name='getenv',
    version='0.1-2',
    url='https://github.com/izznogooood/getenv',
    license='MIT',
    author='Anders Magnus Andersen',
    author_email='ama @ getmail.no',
    description='Keep track of your .env files',
    long_description=get_long_description(),
    py_modules=['getenv'],
    install_requires=[
        'colorama',
        'termcolor'
      ],
    entry_points={
        'console_scripts': [
            'getenv = getenv:main'
        ]
    },
)
