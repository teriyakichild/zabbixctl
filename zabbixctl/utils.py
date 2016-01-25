import getpass
import argparse
import pickle
import logging
import sys


class Cache:

    def __init__(self, cachefile):
        self.cachefile = cachefile

    def get(self, host):
        try:
            token_data = pickle.load(open(self.cachefile, 'rb'))
            token = token_data.get(host, None)
        except IOError:
            token = None
        return token

    def write(self, host, token):
        try:
            token_data = pickle.load(open(self.cachefile, 'rb'))
        except IOError:
            token_data = {}
        token_data[host] = token
        pickle.dump(token_data, open(self.cachefile, 'wb'))


def getlogger():
    log = logging.getLogger('zabbixctl')
    log.addHandler(logging.StreamHandler(sys.stdout))
    log.setLevel(logging.INFO)
    logging.captureWarnings(True)
    return log


def build_parsers():
    """Build parsers for cli"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Zabbix CLI')
    parser.add_argument('-v', '--version',
                        dest='show_version',
                        help='Display version information', action='store_true')
    parser.add_argument('-d', '--debug',
                        dest='debug',
                        help='increase output verbosity', action='store_true')
    parser.add_argument('-i', '--http',
                        help='Use http instead of https', action='store_true')
    parser.add_argument('-V', '--noverify',
                        dest='noverify',
                        help='Do not verify the SSL', action='store_true')
    parser.add_argument('-c', '--cacert',
                        dest='cacert',
                        help='Path to the SSL CA Certificate'
                        'example: /etc/pki/tls/certs/ca-bundle.crt')
    parser.add_argument('-t', '--timeout',
                        dest='timeout',
                        default=30,
                        type=float,
                        help='Zabbix API read timeout in seconds')
    parser.add_argument('-H', '--hosts',
                        dest='hosts',
                        help='Zabbix API host(s).'
                        'example: zabbixhost.example.com', action='append')
    parser.add_argument('-U', '--user',
                        default=getpass.getuser(),
                        help='Zabbix API user')

    subparsers = parser.add_subparsers(dest='subparser_name',)

    get_parser = subparsers.add_parser('get', help='Zabbix API Method for get')
    get_parser.add_argument('type',
                            help='Zabbix API get method (host.get,'
                            'hostgroups.get,usergroups.get)')
    get_parser.add_argument('-a', '--arguments',
                            dest='arguments',
                            default=['output=extend', ],
                            help='RPC params', action='append')

    export_parser = subparsers.add_parser(
        'export', help='Zabbix API Method for export')
    export_parser.add_argument('type',
                               help='Zabbix API export method (host.export,'
                               'hostgroups.export,usergroups.export)')
    export_parser.add_argument('-a', '--arguments',
                               dest='arguments',
                               help='RPC params', action='append')

    update_parser = subparsers.add_parser(
        'update', help='Zabbix API Method for update')
    update_parser.add_argument('type',
                               help='Zabbix API update method (host.update,'
                               'hostgroups.update,usergroups.update)')
    update_parser.add_argument('-a', '--arguments',
                               dest='arguments',
                               help='RPC params', action='append')

    create_parser = subparsers.add_parser(
        'create', help='Zabbix API Method for create')
    create_parser.add_argument('type',
                               help='Zabbix API get method (host.create,'
                               'hostgroups.create,usergroups.create)')
    create_parser.add_argument('-a', '--arguments',
                               dest='arguments',
                               help='RPC params', action='append')

    delete_parser = subparsers.add_parser(
        'delete', help='Zabbix API Method for delete')
    delete_parser.add_argument('type',
                               help='Zabbix API get method (host.delete,'
                               'hostgroups.delete,usergroups.delete)')
    delete_parser.add_argument('-a', '--arguments',
                               dest='arguments',
                               help='RPC params', action='append')

    help_parser = subparsers.add_parser(
        'help', help='Display link for Zabbix wiki')
    help_parser.add_argument('type',
                             help='Displays link for Zabbix Wiki')

    return parser
