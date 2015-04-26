from pyzabbix import ZabbixAPI, ZabbixAPIException
import json
import getpass
import sys
from utils import Cache

c = Cache('/tmp/zabbix.cache')

class Zabbix(object):
    status = True
    error = None
    def __init__(self, host, verify='true'):
        self.zapi = ZabbixAPI('https://{0}/zabbix'.format(host))
        if verify.lower() in ['true','false']:
            verify = eval(verify.title())
        self.zapi.session.verify = verify
        self.host = host
        token = c.get(host)
        if token:
            self.zapi.auth = token
            try:
                test = self.zapi.apiinfo.version()
            except ZabbixAPIException as e:
                if 'Not authorized' in str(e):
                    self.status = False
                else:
                    print e
        else:
            self.status = False

    def status(self):
        return self.status
    
    def auth(self, username, password):
        try:
            self.zapi.login(username, password)
            self.error = None
            self.status = True
            c.write(self.host, self.zapi.auth)
        except ZabbixAPIException as e:
           if e.__class__.__name__ == 'HTTPError' and e.response.status_code == 404:
                self.error = 'Invalid URL'
                self.status = False
                return False
           else:
                self.error = e
                self.status = False
                return False
        return True

    def parse_args(self, args):
        arguments = {}
        if args is not None:
            for argument in args:
                if '=' in argument:
                    tmp = [a for a in argument.split('=',1)]
                    try:
                        value = eval(tmp[1])
                    except (NameError, SyntaxError):
                        value = tmp[1]
                    arguments[tmp[0]] = value
                else:
                    arguments = eval(argument)
        return arguments




#def authenticate(zapi):
#    # Prompt for username and password
#    username = raw_input('Username[{0}]:'.format(getpass.getuser())) or getpass.getuser()
#    password = getpass.getpass()
#
#    # Login to the Zabbix API
#    try:
#        zapi.login(username, password)
#    except Exception as e:
#        if e.__class__.__name__ == 'HTTPError' and e.response.status_code == 404:
#            print 'Invalid URL'
#            exit(1)
#        else:
#            print e
#            exit(1)
#    return zapi.auth

#def main():
#
#    zapi = ZabbixAPI('https://zabbix.dev.ord1.us.ci.rackspace.net/zabbix')
#    zapi.session.verify = False
#
#    c = Cache('/tmp/zabbix.cache')
#    token = c.get(sys.argv[1])
#    if token:
#        zapi.auth = token
#        try:
#            test = zapi.apiinfo.version()
#        except ZabbixAPIException as e:
#            if 'Not authorized' in str(e):
#                token = authenticate(zapi)
#                c.write(sys.argv[1],token)
#            else:
#                print e
#    else:
#        token = authenticate(zapi)
#        c.write(sys.argv[1], token)

if __name__ == '__main__':
    Z = Zabbix('zabbix.dev.ord1.us.ci.rackspace.net')
    username = getpass.getuser()
    password = getpass.getpass()
    Z.auth(username, password)
    import pdb;pdb.set_trace()
