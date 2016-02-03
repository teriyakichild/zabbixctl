"""zabbixctl - CLI for Zabbix API"""

__version__ = '1.1.0'

import json
import getpass
import sys
from utils import build_parsers, parse_args
import logging
from Zabbix import Zabbix, ZabbixNotAuthorized, ZabbixError
from datetime import datetime

log = logging.getLogger(__name__)

# todo: lets move main out of __init__ and into it's own file. Keep version
# and basic stuff in here


def main(args=None):
    parser = build_parsers(version=__version__)

    if args is None:
        try:
            args = parser.parse_args(sys.argv[1:])
        except IOError as e:
            log.error("Could not open file %s: %s" %
                      (e.filename, e.strerror))
            exit(1)

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("Debug enabled")

    method_type = getattr(args, 'type')
    method = getattr(args, 'subparser_name')

    if method not in ['help']:
        Z = {}
        rets = {}
        for host in args.hosts:
            count = 0
            Z[host] = Zabbix(host, args.user, args.noverify, args.cacert,
                             args.http, args.timeout)
            # allow the user to auth 3 times before returning an error
            while count < 3 and Z[host].zapi.auth == '':
                try:
                    Z[host].auth(args.user, getpass.getpass())
                    # if successful, break out of the loop
                    break
                except ZabbixNotAuthorized:
                    pass
                count = count + 1
            if Z[host].zapi.auth == '':
                raise ZabbixNotAuthorized('Invalid username or password')

            func = getattr(
                getattr(getattr(Z[host], 'zapi'), method_type), method)

            # If the listkeys argument was supplied, we need to override
            # args.arguments to pull one resource
            if args.listkeys:
                args.arguments = ['output=extend', 'limit=1']

            args_real = parse_args(args.arguments)

            if type(args_real) == str or type(args_real) == int:
                rets[host] = func(str(args_real))
            elif type(args_real) == list:
                rets[host] = func(*args_real)
            else:
                rets[host] = func(**args_real)
        final = []
        for ret in rets:
            # if the results are not a list, the final output should be final
            # this was added to support the configuration.export method of the
            # API
            if type(rets[ret]) == list:
                final += rets[ret]
            elif type(rets[ret]) == dict:
                final = rets[ret]
            else:
                final = eval(rets[ret])

        if any(method_type in s for s in ['alert']):
            final = sorted(final, key=lambda k: k['clock'])

        # If there is a timestamp we want to do stuff to it
        if method not in ['create', 'delete', 'update', 'export']:
            # Check if one of the following keys exist
            list_of_checks = ['clock', 'lastchange']
            matched_check = None
            for check in list_of_checks:
                try:
                    if final[0].get(check, None):
                        matched_check = check
                except IndexError:
                    pass
        else:
            matched_check = None

        # If a key exists, then sort on that key and update the unix_timestamp
        # to readable format
        if matched_check:
            final = sorted(final, key=lambda k: k[matched_check])
            for item in final:
                item[matched_check] = str(
                    datetime.fromtimestamp(float(item[matched_check])))
        # if the "listkeys" argument was supplied, we should return the
        # keys of the first resource in the list.
        if args.listkeys:
            sys.stdout.write(json.dumps(final[0].keys(), indent=2))
        else:
            sys.stdout.write(json.dumps(final, indent=2))
    else:
        log.info(
            'https://www.zabbix.com/documentation/2.2/manual/api/reference/{0}'.format(method_type))

if __name__ == '__main__':
    main()
