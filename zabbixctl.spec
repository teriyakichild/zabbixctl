%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define module_name zabbixctl

Name:           %{module_name}
Version:        0.1.0
Release:        1
Summary:        zabbixctl - Utility that connects to Zabbix API

License:        ASLv2
URL:            https://github.com/teriyakichild/zabbixctl
Source0:        %{module_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools


%description

%prep
%setup -q -n %{module_name}-%{version}


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%doc README.md
%{python_sitelib}/*
%attr(0755,-,-) %{_bindir}/zabbixctl

%changelog
* Mon Sep 8 2014 Tony Rogers <tony.rogers@rackspace.com> - 0.1.0
- Initial spec
