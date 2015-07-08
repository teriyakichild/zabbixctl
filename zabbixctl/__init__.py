"""zabbixctl - CLI for Zabbix API"""
import json
import getpass
import sys
from utils import Cache, build_parsers
from Zabbix import Zabbix
from datetime import datetime

def main(args=None):
    parser = build_parsers()

    if args is None:
        try:
            args = parser.parse_args(sys.argv[1:])

        except IOError as e:
            print("Could not open file %s: %s" % (e.filename, e.strerror))
            exit(1)

    if args.debug:
        print("Debug enabled")

    method_type = getattr(args, 'type')
    method = getattr(args, 'subparser_name')
 
    if method not in ['help']:
        Z = {}
        rets = {}
        for host in args.hosts:
            Z[host] = Zabbix(host, args.verify)
            if Z[host].status:
                pass
            else:
                Z[host].auth(args.user, getpass.getpass())
            func =  getattr(getattr(getattr(Z[host], 'zapi'), method_type), method)
            args_real = Z[host].parse_args(args.arguments)
            if type(args_real) == str or type(args_real) == int:
                rets[host] = func(str(args_real))
            elif type(args_real) == list:
                rets[host] = func(*args_real)
            else:
                rets[host] = func(**args_real)
        final = []
        for ret in rets:
            # if the results are not a list, the final output should be final
            # this was added to support the configuration.export method of the API
            if type(rets[ret]) == list:
                final += rets[ret]
            else:
                final = eval(rets[ret])

        if any(method_type in s for s in ['alert']):
            final = sorted(final, key=lambda k: k['clock']) 

        # If there is a timestamp we want to do stuff to it
        if method not in ['create', 'delete', 'update', 'export']:
            # Check if one of the following keys exist
            list_of_checks = [ 'clock','lastchange' ]
            matched_check = None
            for check in list_of_checks:
                try:
                    if final[0].get(check, None):
                        matched_check = check
                except IndexError:
                    pass
        else:
            matched_check = None

        # If a key exists, then sort on that key and update the unix_timestamp to readable format
        if matched_check:
            final = sorted(final, key=lambda k: k[matched_check])
            for item in final:
                item[matched_check] = str(datetime.fromtimestamp(float(item[matched_check])))
        return json.dumps(final, indent=2)
    else:
        print 'https://www.zabbix.com/documentation/2.2/manual/api/reference/{0}'.format(method_type)

if __name__ == '__main__':
    main()
