from setuptools import setup
from sys import path

path.insert(0, '.')

NAME = "zabbixctl"

if __name__ == "__main__":

    setup(
        name = NAME,
        version = "1.0.0",
        author = "Tony Rogers",
        author_email = "tony.rogers@rackspace.com",
        url = "https://github.com/teriyakichild/zabbixctl",
        license = 'ASLv2',
        packages = [NAME],
        package_dir = {NAME: NAME},
        description = "zabbixctl - Utility that connects to Zabbix API",

        install_requires = ['requests>=2.0.0',
                            'argparse',
                            'pyzabbix',
                            'ConfigParser'],
        entry_points={
            'console_scripts': [ 'zabbixctl = zabbixctl:main' ],
        }
    )

