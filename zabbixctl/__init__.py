"""zabbixctl - CLI for Zabbix API"""
import json
import getpass
import sys
from utils import Cache, build_parsers
from Zabbix import Zabbix
from datetime import datetime

def main():
    parser = build_parsers()

    try:
        args = parser.parse_args(sys.argv[1:])

    except IOError as e:
        print("Could not open file %s: %s" % (e.filename, e.strerror))
        exit(1)

    if args.debug:
        print("Debug enabled")

    Z = {}
    rets = {}
    for host in args.hosts:
        Z[host] = Zabbix(host)
        if Z[host].status:
            pass
        else:
            Z[host].auth(args.user, getpass.getpass())
        method_type = getattr(args, 'type')
        method = getattr(args, 'subparser_name')
        func =  getattr(getattr(getattr(Z[host], 'zapi'), method_type), method)
        rets[host] = func(**Z[host].parse_args(args.arguments))
    final = []
    for ret in rets:
        final += rets[ret]

    if any(method_type in s for s in ['alert']):
        final = sorted(final, key=lambda k: k['clock']) 

    list_of_checks = [ 'clock','lastchange' ]
    matched_check = None
    for check in list_of_checks:
        if final[0].get(check, None):
            matched_check = check

    if matched_check:
        # If there is a clock, then sort based on that field
        final = sorted(final, key=lambda k: k[matched_check])
        # Now we are going to convert the uniz timestamp to a readable format
        for item in final:
            item[matched_check] = str(datetime.fromtimestamp(float(item[matched_check])))
        
    print json.dumps(final, indent=2)

if __name__ == '__main__':
    main()
