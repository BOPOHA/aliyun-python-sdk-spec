# Created by pyp2rpm-3.3.2
%global pypi_name aliyun-python-sdk-alidns

Name:           python-%{pypi_name}
Version:        2.0.18
Release:        1%{?dist}
Summary:        The alidns module of Aliyun Python sdk

License:        Apache
URL:            http://develop.aliyun.com/sdk/python
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 aliyun-python-sdk-alidns .. This is the alidns module of Aliyun Python
SDK.Aliyun Python SDK is the official software development kit. It makes things
easy to integrate your Python application, library, or script with Aliyun
services.This module works on Python versions:2.6.5 and
greater**Documentation:**Please visit <

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(aliyun-python-sdk-core) >= 2.11.5
%description -n python3-%{pypi_name}
 aliyun-python-sdk-alidns .. This is the alidns module of Aliyun Python
SDK.Aliyun Python SDK is the official software development kit. It makes things
easy to integrate your Python application, library, or script with Aliyun
services.This module works on Python versions:2.6.5 and
greater**Documentation:**Please visit <


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.rst
%{python3_sitelib}/aliyunsdkalidns
%{python3_sitelib}/aliyun_python_sdk_alidns-%{version}-py?.?.egg-info

%changelog
* Wed May 27 2020 mockbuilder - 2.0.18-1
- Initial package.