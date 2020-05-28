# Created by pyp2rpm-3.3.2
%global pypi_name oss2

Name:           python-%{pypi_name}
Version:        2.11.0
Release:        1%{?dist}
Summary:        Aliyun OSS (Object Storage Service) SDK

License:        None
URL:            http://oss.aliyun.com
Source0:        https://files.pythonhosted.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildConflicts: python3dist(requests) = 2.9.0
BuildRequires:  python3dist(aliyun-python-sdk-core) >= 2.5.5
BuildRequires:  python3dist(aliyun-python-sdk-kms) >= 2.4.1
BuildRequires:  python3dist(crcmod) >= 1.7
BuildRequires:  python3dist(pycryptodome) >= 3.4.7
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)

%description
Alibaba Cloud OSS SDK for Python README of Chinese < Alibaba Cloud Object
Storage Python SDK 2.x. This version is not compatible with the previous
version (Version 0.x). The package name is oss2 to avoid conflict with previous
versions.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Conflicts:      python3dist(requests) = 2.9.0
Requires:       python3dist(aliyun-python-sdk-core) >= 2.5.5
Requires:       python3dist(aliyun-python-sdk-kms) >= 2.4.1
Requires:       python3dist(crcmod) >= 1.7
Requires:       python3dist(pycryptodome) >= 3.4.7
%description -n python3-%{pypi_name}
Alibaba Cloud OSS SDK for Python README of Chinese < Alibaba Cloud Object
Storage Python SDK 2.x. This version is not compatible with the previous
version (Version 0.x). The package name is oss2 to avoid conflict with previous
versions.


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu May 28 2020 mockbuilder - 2.11.0-1
- Initial package.