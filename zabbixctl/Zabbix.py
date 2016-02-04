"""Contains all the classes and functions associated with the Zabbix object
type"""
# Standard Lib
import getpass
import logging
from utils import Cache
from urlparse import urlunparse, urljoin

# Packages
from pyzabbix import ZabbixAPI, ZabbixAPIException
from requests.exceptions import HTTPError, ConnectionError

log = logging.getLogger(__name__)


class ZabbixError(Exception):
    pass


class ZabbixNotAuthorized(ZabbixError):
    pass


class Zabbix(object):

    def __init__(self, host, uri_path, user, noverify=False, cacert=None, http=False, timeout=30):
        """
        Initializes a Zabbix instance
        :param host: hostname to connect to (ex. zabbix.yourdomain.net)
        :param user: username to connect with (ex. Admin)
        :param uri_path: uri path to zabbix api (ex. zabbix)
        :param noverify: turns off verification
        :param cacert: the certificate authority to use
        :param http: flag to use http over https
        :param timeout: API timeout parameter
        :return: Zabbix instance
        """

        self.cache = Cache('/tmp/zabbix.cache')
        self.host = host
        self.cache_slug = '{0}-{1}'.format(host, user)

        zabbix_url = urlunparse([
            'http' if http else 'https',
            host.strip('/'),
            uri_path,
            '', '', ''
        ]
        )
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
        self.fetch_zabbix_api_version()  # Check the api

        token = self.cache.get(self.cache_slug)
        if token:
            log.debug('Found token for {0}'.format(host))
            self.zapi.auth = token
            # Let's test the token
            try:
                self.verify_token()
            except ZabbixNotAuthorized:
                self.zapi.auth = ''
                self.cache.delete(self.cache_slug)

    def fetch_zabbix_api_version(self):
        """
        reaches out to the zapi api info to parse the string
        :return: Version string or False
        """
        try:
            return self.zapi.apiinfo.version()
        except (HTTPError, ConnectionError, ZabbixAPIException) as e:
            raise ZabbixError(e)

    def verify_token(self):
        """
        Runs the zapi.host.get(limit=1) call to test the current token
        :return: Nothing
        """
        try:
            self.zapi.host.get(limit=1)
        except (HTTPError, ConnectionError, ZabbixAPIException) as e:
            # todo: cant we check by the error, not its string?
            if any(['Not authorised' in str(e),
                    'Not authorized' in str(e),
                    'Session terminated,' in str(e)]):
                log.debug('Token not authorized for {0}'.format(self.host))
                raise ZabbixNotAuthorized
            raise ZabbixError(e)

    def auth(self, username, password):
        """
        Performs the loggin function of the api with the supplied credentials
        :param username: username
        :param password: password
        :return: True is valid, False otherwise
        """
        try:
            self.zapi.login(username, password)
            self.cache.write(self.cache_slug, self.zapi.auth)
        except ZabbixAPIException as e:
            raise ZabbixNotAuthorized('Username or password invalid')
        return True


if __name__ == '__main__':
    Z_obj = Zabbix('zabbix.yourdomain.net')
    username = getpass.getuser()
    password = getpass.getpass()
    Z_obj.auth(username, password)
    import pdb
    pdb.set_trace()
