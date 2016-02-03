"""zabbixctl - CLI for Zabbix API"""

__version__ = '1.1.0'

import logging
import sys

from cli import ZabbixCLI

log = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.INFO)
logging.captureWarnings(True)


def main(args=None):
    cli = ZabbixCLI(__version__)
    cli.load(sys.argv[1:])
    cli.auth()
    cli.execute()

if __name__ == '__main__':
    main()
