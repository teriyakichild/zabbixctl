from pyzabbix import ZabbixAPI, ZabbixAPIException
import getpass
import logging
from utils import Cache
from requests.exceptions import HTTPError, ConnectionError

#todo: don't we want an instance cache not a global one?
cache = Cache('/tmp/zabbix.cache')

log = logging.getLogger(__name__)


class Zabbix(object):

    def __init__(self, host, noverify=False, cacert=None, http=False, timeout=30):
        """
        Initializes a Zabbix instance
        :param host: hostname to connect to (ex. zabbix.yourdomain.net)
        :param noverify: turns off verification
        :param cacert: the certificate authority to use
        :param http: flag to use http over https
        :param timeout: API timeout parameter
        :return: Zabbix instance
        """

        # todo: instead of setting object attricutes and checking them later
        # why not raise exception and catch in code above?
        self.status = True
        self.error = None

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
        token = cache.get(host)
        if token:
            log.debug('Found token for {0}'.format(host))
            self.zapi.auth = token
            # Let's test the token by grabbing the api version
            self.fetch_zabbix_api_version()
        else:
            self.status = False

    def fetch_zabbix_api_version(self):
        """
        reaches out to the zapi api info to parse the string
        :return: Version string or False
        """
        try:
            return self.zapi.apiinfo.version()

        except ZabbixAPIException as e:
            log.exception(e)
            self.status = False
            self.error = e
            # todo: cant we check by the error, not its string?
            if 'Not authorized' in str(e):
                log.debug('Token not authorized for {0}'.format(self.host))
        except (HTTPError, ConnectionError) as e:
            log.exception(e)
            self.error = e
        return False

    def auth(self, username, password):
        """
        Performs the loggin function of the api with the supplied credentials
        :param username: username
        :param password: password
        :return: True is valid, False otherwise
        """
        try:
            self.zapi.login(username, password)
            self.error = None
            self.status = True
            cache.write(self.host, self.zapi.auth)
        except ZabbixAPIException as e:
            log.exception(e)
            self.error = e
            self.status = False
            return False
        return True

    # todo: why is this part of the zabbix object? if it's parsing the command
    # line arguments it should be par of the command line code
    def parse_args(self, args):
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

if __name__ == '__main__':
    Z_obj = Zabbix('zabbix.yourdomain.net')
    username = getpass.getuser()
    password = getpass.getpass()
    Z_obj.auth(username, password)
    import pdb
    pdb.set_trace()
