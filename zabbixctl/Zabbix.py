from pyzabbix import ZabbixAPI, ZabbixAPIException
import json
import getpass
import sys
import logging
from utils import Cache
from requests.exceptions import HTTPError, ConnectionError
#import urllib3

c = Cache('/tmp/zabbix.cache')


class Zabbix(object):
    status = True
    error = None

    def __init__(self, host, noverify=False, cacert=None, http=False, timeout=30):
        self.logger = logging.getLogger('zabbixctl')
        self.zabbix_url = host
        protocol = 'http' if http else 'https'

        self.zabbix_url = '{0}://{1}/zabbix'.format(protocol, host)

        self.logger.debug(self.zabbix_url)

        self.zapi = ZabbixAPI(self.zabbix_url)

        if cacert is not None:
            self.logger.debug(
                'Setting zapi.session.verify to {0}'.format(cacert))
            self.zapi.session.verify = cacert

        if noverify:
            self.logger.debug('Setting zapi.session.verify to False')
            self.zapi.session.verify = False

        self.zapi.timeout = timeout
        self.fetch_zabbix_api_version()

        self.host = host
        token = c.get(host)
        if token:
            self.logger.debug('Found token for {0}'.format(host))
            self.zapi.auth = token
            # Let's test the token by grabbing the api version
            self.fetch_zabbix_api_version()
        else:
            self.status = False

    def fetch_zabbix_api_version(self):
        try:
            return self.zapi.apiinfo.version()
        except ZabbixAPIException as e:
            self.status = False
            if 'Not authorized' in str(e):
                self.logger.debug('Token not authorized for {0}'.format(host))
                self.error = e
            else:
                self.error = e
        except (HTTPError, ConnectionError) as e:
            self.error = e
        return False

    def status(self):
        return self.status

    def auth(self, username, password):
        try:
            self.zapi.login(username, password)
            self.error = None
            self.status = True
            c.write(self.host, self.zapi.auth)
        except ZabbixAPIException as e:
            self.error = e
            self.status = False
            return False
        return True

    def parse_args(self, args):
        arguments = {}
        if args is not None:
            for argument in args:
                if '=' in argument:
                    tmp = [a for a in argument.split('=', 1)]
                    try:
                        value = eval(tmp[1])
                    except (NameError, SyntaxError):
                        value = tmp[1]
                    arguments[tmp[0]] = value
                else:
                    arguments = eval(argument)
        return arguments

if __name__ == '__main__':
    Z = Zabbix('zabbix.yourdomain.net')
    username = getpass.getuser()
    password = getpass.getpass()
    Z.auth(username, password)
    import pdb
    pdb.set_trace()
