# Created by pyp2rpm-3.3.2
%global pypi_name aliyun-python-sdk-core

Name:           python-%{pypi_name}
Version:        2.13.16
Release:        4%{?dist}
Summary:        The core module of Aliyun Python SDK

License:        Apache License 2.0
URL:            https://github.com/aliyun/aliyun-openapi-python-sdk
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 aliyun-python-sdk-core This is the core module of Aliyun Python SDK.Aliyun
Python SDK is the official software development kit. It makes things easy to
integrate your Python application, library, or script with Aliyun services.This
module works on Python versions: * 2.6.5 and greater Documentation:Please visit

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(jmespath) < 1.0.0
Requires:       python3dist(jmespath) >= 0.9.3
Requires:       python3dist(pycryptodome) >= 3.4.7
Provides:       python3dist(%{pypi_name}-v3)

%description -n python3-%{pypi_name}
 aliyun-python-sdk-core This is the core module of Aliyun Python SDK.Aliyun
Python SDK is the official software development kit. It makes things easy to
integrate your Python application, library, or script with Aliyun services.This
module works on Python versions: * 2.6.5 and greater Documentation:Please visit


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
%{python3_sitelib}/aliyunsdkcore
%{python3_sitelib}/aliyun_python_sdk_core-%{version}-py?.?.egg-info

%changelog
* Wed May 27 2020 mockbuilder - 2.13.16-1
- Initial package.