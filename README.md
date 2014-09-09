# zabbixctl

## Install

sudo make install
or
sudo python setup.py install

## Usage
```
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
```
