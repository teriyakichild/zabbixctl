from datetime import datetime
import getpass
import json
import logging
import sys


from Zabbix import Zabbix, ZabbixNotAuthorized
from utils import build_parsers, parse_args
from zabbixctl import __version__ as version

log = logging.getLogger(__name__)


class ZabbixCLI(object):
    METHOD_TYPE = None
    METHOD = None
    JOBS = None
    HOSTS = None

    def __init__(self, version):
        self._args = None
        self._parser = build_parsers(version=version)
        self.JOBS = {}
        self.HOSTS = {}

    def load(self, parser_args):
        try:
            # parse the supplied args with ConfigParser.parse_args
            self._args = self._parser.parse_args(parser_args)
        except IOError as e:
            log.error("Could not open file %s: %s" %
                      (e.filename, e.strerror))
            exit(1)

        if self._args.debug:
            log.setLevel(logging.DEBUG)
            log.debug("Debug enabled")
        self.METHOD_TYPE = getattr(self._args, 'type')
        self.METHOD = getattr(self._args, 'subparser_name')

        if self.METHOD not in ['help']:
            self.HOSTS = {}
            rets = {}
            for host in self._args.hosts:
                self.HOSTS[host] = Zabbix(
                    host,
                    self._args.uri_path,
                    self._args.user,
                    self._args.noverify,
                    self._args.cacert,
                    self._args.http,
                    self._args.timeout
                )
                zapi_function = getattr(
                    getattr(getattr(self.HOSTS[host], 'zapi'), self.METHOD_TYPE), self.METHOD)

                # If the listkeys argument was supplied, we need to override
                # args.arguments to pull one resource
                if getattr(self._args, 'listkeys', False):
                    self._args.arguments = ['output=extend', 'limit=1']
                # convert the arguments into the required format for the zapi
                # object.
                args_real = parse_args(self._args.arguments)

                # Parse specific cli arguments and update args_real
                args_to_parse = ['search', 'filter']
                for key in args_to_parse:
                    if getattr(self._args, key, None) is not None:
                        args_real[key] = parse_args(getattr(self._args, key))

                self.JOBS[host] = (zapi_function, args_real)

    def auth(self):
        for host, zbx in self.HOSTS.items():
            count = 0
            while count < 3 and zbx.zapi.auth == '':
                try:
                    zbx.auth(self._args.user, getpass.getpass())
                    # if successful, break out of the loop
                    break
                except ZabbixNotAuthorized:
                    pass
                count += 1
            if zbx.zapi.auth == '':
                log.exception(ZabbixNotAuthorized(
                    'Invalid username or password for {0}'.format(host)))

    def execute(self):
        if self.METHOD not in ['help']:
            final = []
            for job, data in self.JOBS.items():
                zapi_function = data[0]
                arguments = data[1]
                if type(arguments) == str or type(arguments) == int:
                    ret = zapi_function(str(arguments))
                elif type(arguments) == list:
                    ret = zapi_function(*arguments)
                else:
                    ret = zapi_function(**arguments)

                if type(ret) == list:
                    final += ret
                elif type(ret) == dict:
                    final = ret
                else:
                    final = eval(ret)

            # if method type is alert, sort based on 'clock' key
            if any(self.METHOD_TYPE in s for s in ['alert']):
                final = sorted(final, key=lambda k: k['clock'])

            if self.METHOD not in ['create', 'delete', 'update', 'export']:
                # Check if one of the following keys exist
                list_of_keys = ['clock', 'lastchange']
                matched_key = None
                for key in list_of_keys:
                    try:
                        if final[0].get(key, None):
                            matched_key = key
                    except KeyError:
                        if final.itervalues().next().get(key, None):
                            matched_key = key
                    except IndexError:
                        pass
                # If a key exists, then sort on that key and update the unix_timestamp
                # to readable format
                if matched_key:
                    final = sorted(final, key=lambda k: k[matched_key])
                    for item in final:
                        item[matched_key] = str(
                            datetime.fromtimestamp(float(item[matched_key]))
                        )
            # if the "listkeys" argument was supplied, we should return the
            # keys of the first resource in the list.
            if getattr(self._args, 'listkeys', False):
                sys.stdout.write(json.dumps(final[0].keys(), indent=2))
            else:
                sys.stdout.write(json.dumps(final, indent=2))
        else:
            log.info(
                'https://www.zabbix.com/documentation/2.2/manual/api/reference/{0}'.format(self.METHOD_TYPE)
            )


def main(args=None):
    handler = logging.StreamHandler(sys.stdout)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    logging.captureWarnings(True)

    cli = ZabbixCLI(version=version)
    cli.load(sys.argv[1:])
    cli.auth()
    cli.execute()
