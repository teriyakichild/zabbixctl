# zabbixctl

## Install
```bash
sudo pip install zabbixctl 
#or 
sudo make install 
#or 
sudo python setup.py install
```

## Usage
```
usage: zabbixctl [-h] [-d] [-i] [-V] [-c CACERT] [-t TIMEOUT] [-H HOSTS]
                 [-U USER]
                 {help,get,create,update,export,delete} ...

Zabbix CLI

positional arguments:
  {help,get,create,update,export,delete}
    get                 Zabbix API Method for get
    export              Zabbix API Method for export
    update              Zabbix API Method for update
    create              Zabbix API Method for create
    delete              Zabbix API Method for delete
    help                Display link for Zabbix wiki

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           increase output verbosity (default: False)
  -i, --http            Use http instead of https (default: False)
  -V, --noverify        Do not verify the SSL (default: False)
  -c CACERT, --cacert CACERT
                        Path to the SSL CA Certificateexample:
                        /etc/pki/tls/certs/ca-bundle.crt (default: None)
  -t TIMEOUT, --timeout TIMEOUT
                        Zabbix API read timeout in seconds (default: 30)
  -H HOSTS, --hosts HOSTS
                        Zabbix API host(s).example: zabbixhost.example.com
                        (default: None)
  -p URI_PATH, --uri-path URI_PATH
                        URI path to zabbix api. default: zabbix (default:
                        zabbix)
  -U USER, --user USER  Zabbix API user (default: system username)

usage: zabbixctl get [-h] [-a ARGUMENTS] type

positional arguments:
  type                  Zabbix API get method
                        (host.get,hostgroups.get,usergroups.get)

optional arguments:
  -h, --help            show this help message and exit
  -a ARGUMENTS, --arguments ARGUMENTS
                        RPC params
  -k, --listkeys        Returns a list of keys for the given resource type
  -f FILTER, --filter FILTER
                        Takes "key=value" args that are sent to the zabbix api
                        in the filter parameter
  -s SEARCH, --search SEARCH
                        Takes "key=value" args that are sent to the zabbix api
                        in the search parameter
```

## Examples
```bash
zabbixctl -H zabbix.yourdomain.com get trigger -a 'hostids=[10167]' -a 'expandExpression=true' -a 'expandDescription=true'
zabbixctl -H zabbix.yourdomain.com get trigger -a 'search={"host":"syslog"}' -a 'expandExpression=true' -a 'searchWildcardsEnabled=true' -a 'selecthosts=extend'
zabbixctl -H zabbix.yourdomain.com get trigger -a 'triggerids=[14924]'
zabbixctl -H zabbix.yourdomain.com get trigger -a 'search={"host":"syslog"}' -a 'expandExpression=true'
zabbixctl -H zabbix.yourdomain.com get user
zabbixctl -H zabbix.yourdomain.com get host
zabbixctl -H zabbix.yourdomain.com get host -a 'search={"host":"syslog"}' -a 'searchWildcardsEnabled=true'
zabbixctl -H zabbix.yourdomain.com get alert -a 'time_from=1409611855' -a 'output=extend'
zabbixctl -H zabbix.yourdomain.com get itemprototype
zabbixctl -H zabbix.yourdomain.com get event -a 'time_from=1409611855' -a 'output=extend' -a 'selectRelatedObject=["description"]'
zabbixctl -H zabbix.yourdomain.com get alert -a 'time_from=1409611855' -a 'output=extend' -a 'selectHosts=["host"]'
zabbixctl -H zabbix.yourdomain.com get template -a 'output=["host"]' -a 'selectItems=extend' -a 'templateids=[10167]'
```

## Known Issues

Error: ImportError: cannot import name to_native_string  
Solution: Upgrade to at least version 2.0 of requests
