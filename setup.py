from setuptools import setup
from sys import path

from zabbixctl import __version__

path.insert(0, '.')

NAME = "zabbixctl"

if __name__ == "__main__":

    with open('requirements.txt') as f:
        requirements = f.read().splitlines()

    setup(
        name=NAME,
        version=__version__,
        author="Tony Rogers",
        author_email="tony.rogers@rackspace.com",
        url="https://github.com/teriyakichild/zabbixctl",
        license='ASLv2',
        packages=[NAME],
        package_dir={NAME: NAME},
        description="zabbixctl - Utility that connects to Zabbix API",

        install_requires=requirements,

        entry_points={
            'console_scripts': ['zabbixctl = zabbixctl.cli:main'],
        }
    )
