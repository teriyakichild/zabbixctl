import getpass
import argparse
import json
import logging
import sys


class Cache:

    def __init__(self, cachefile):
        self.cachefile = cachefile

    def __get_token_data(self):
        try:
            token_data = json.load(open(self.cachefile, 'rb'))
        except (IOError, ValueError):
            token_data = {}
        return token_data

    def __write_token_data(self, data):
        json.dump(data, open(self.cachefile, 'wb'))

    def get(self, slug):
        """
        Get token from cache
        :param slug: unique key to store in cache.  Should be 'host-user'.
        """
        return self.__get_token_data().get(slug, None)

    def write(self, slug, token):
        token_data = self.__get_token_data()
        token_data[slug] = token
        self.__write_token_data(token_data)

    def delete(self, slug):
        token_data = self.__get_token_data()
        token_data.pop(slug, None)
        self.__write_token_data(token_data)


def build_parsers(version):
    """Build parsers for cli"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Zabbix CLI')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {0}'.format(version))
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
                        required=True,
                        help='Zabbix API host(s).'
                        'example: zabbixhost.example.com', action='append')
    parser.add_argument('-p', '--uri-path',
                        dest='uri_path',
                        default='zabbix',
                        help='URI path to zabbix api. default: zabbix')
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
    get_parser.add_argument('-k', '--listkeys',
                            dest='listkeys',
                            default=False,
                            help='Returns a list of keys for the '
                            'given resource type', action='store_true')
    get_parser.add_argument('-f', '--filter',
                            dest='filter',
                            help='Takes "key=value" args that are sent to the'
                            ' zabbix api in the filter parameter', action='append')
    get_parser.add_argument('-s', '--search',
                            dest='search',
                            help='Takes "key=value" args that are sent to the'
                            ' zabbix api in the search parameter', action='append')

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


def parse_args(args):
    """
    Takes the given args, parses them and return the arguments object
    :param args:
    :return:
    """
    arguments = {}
    if args is not None:
        for argument in args:
            if '=' in argument:
                tmp = [a for a in argument.split('=', 1)]
                try:
                    value = eval(tmp[1])  # todo: this seems dangerous
                except (NameError, SyntaxError):
                    value = tmp[1]
                arguments[tmp[0]] = value
            else:
                arguments = eval(argument)
    return arguments
