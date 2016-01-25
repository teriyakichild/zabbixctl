from pyzabbix import ZabbixAPI, ZabbixAPIException
import getpass
import logging
from utils import Cache
from requests.exceptions import HTTPError, ConnectionError

c = Cache('/tmp/zabbix.cache')

log = logging.getLogger(__name__)

class Zabbix(object):
    STATUS = True
    ERROR = None

    def __init__(self, host, noverify=False, cacert=None, http=False, timeout=30):
        """

        :param host:
        :param noverify:
        :param cacert:
        :param http:
        :param timeout:
        :return: Zabbix instance
        """

        protocol = 'http' if http is True else 'https'
        zabbix_url = '{0}://{1}/zabbix'.format(protocol, host)
        log.debug("Creating instance of Zabbic with url: %s", zabbix_url)

        self.zapi = ZabbixAPI(zabbix_url)

        if cacert is not None:
            log.debug('Setting zapi.session.verify to {0}'
                      ''.format(cacert))
            self.zapi.session.verify = cacert

        if noverify:
            log.debug('Setting zapi.session.verify to False')
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
    Z_obj = Zabbix('zabbix.yourdomain.net')
    username = getpass.getuser()
    password = getpass.getpass()
    Z_obj.auth(username, password)
    import pdb
    pdb.set_trace()
