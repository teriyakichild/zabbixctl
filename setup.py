from setuptools import setup
from sys import path

path.insert(0, '.')

NAME = "zabbixctl"

if __name__ == "__main__":

    setup(
        name = NAME,
        version = "0.1.1",
        author = "Tony Rogers",
        author_email = "tony.rogers@rackspace.com",
        url = "https://github.com/teriyakichild/zabbixctl",
        license = 'internal use',
        packages = [NAME],
        package_dir = {NAME: NAME},
        description = "zabbixctl - Utility that connects to Zabbix API",

        install_requires = ['requests',
                            'argparse',
                            'pyzabbix',
                            'ConfigParser'],
        entry_points={
            'console_scripts': [ 'zabbixctl = zabbixctl:main' ],
        }
    )

