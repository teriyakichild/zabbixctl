"""zabbixctl - CLI for Zabbix API"""
from cli import main

__version__ = '1.1.0'
__all__ = ["cli", "utils", "Zabbix"]

if __name__ == '__main__':
    main()
