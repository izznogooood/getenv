from setuptools import setup

from config import VERSION


# noinspection PyBroadException
def get_long_description():
    try:
        with open("README.md", "r") as f:
            return f.read()
    except:
        return ""


setup(
    name="getenv",
    version=VERSION,
    url="https://github.com/izznogooood/getenv",
    license="MIT",
    author="Anders Magnus Andersen",
    author_email="ama @ getmail.no",
    description="Keep track of your .env files",
    long_description=get_long_description(),
    py_modules=["getenv", "config"],
    install_requires=["colorama", "termcolor", "requests"],
    entry_points={"console_scripts": ["getenv = getenv:main"]},
)
