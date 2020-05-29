# Created by pyp2rpm-3.3.2
%global pypi_name footmark

Name:           python-%{pypi_name}
Version:        1.20.0
Release:        1%{?dist}
Summary:        A Python interface to Aliyun Web Services

License:        MIT
URL:            https://github.com/alibaba/footmark
Source0:        https://files.pythonhosted.org/packages/source/f/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(aliyun-python-sdk-alidns) >= 2.0.11
BuildRequires:  python3dist(aliyun-python-sdk-core) >= 2.13.10
BuildRequires:  python3dist(aliyun-python-sdk-ecs) >= 4.18.3
BuildRequires:  python3dist(aliyun-python-sdk-ess) >= 2.1.3
BuildRequires:  python3dist(aliyun-python-sdk-market) >= 2.0.24
BuildRequires:  python3dist(aliyun-python-sdk-oos) >= 1.1.0
BuildRequires:  python3dist(aliyun-python-sdk-ram) >= 3.1.0
BuildRequires:  python3dist(aliyun-python-sdk-rds) >= 2.1.0
BuildRequires:  python3dist(aliyun-python-sdk-ros) = 3.2.0
BuildRequires:  python3dist(aliyun-python-sdk-slb) >= 3.2.16
BuildRequires:  python3dist(aliyun-python-sdk-sts) >= 2.1.7
BuildRequires:  python3dist(aliyun-python-sdk-vpc) >= 3.0.7
BuildRequires:  python3dist(oss2) >= 2.3.3
BuildRequires:  python3dist(setuptools)

%description
A Python interface to Aliyun Web Services

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(aliyun-python-sdk-alidns) >= 2.0.11
Requires:       python3dist(aliyun-python-sdk-core) >= 2.13.10
Requires:       python3dist(aliyun-python-sdk-ecs) >= 4.18.3
Requires:       python3dist(aliyun-python-sdk-ess) >= 2.1.3
Requires:       python3dist(aliyun-python-sdk-market) >= 2.0.24
Requires:       python3dist(aliyun-python-sdk-oos) >= 1.1.0
Requires:       python3dist(aliyun-python-sdk-ram) >= 3.1.0
Requires:       python3dist(aliyun-python-sdk-rds) >= 2.1.0
Requires:       python3dist(aliyun-python-sdk-ros) = 3.2.0
Requires:       python3dist(aliyun-python-sdk-slb) >= 3.2.16
Requires:       python3dist(aliyun-python-sdk-sts) >= 2.1.7
Requires:       python3dist(aliyun-python-sdk-vpc) >= 3.0.7
Requires:       python3dist(oss2) >= 2.3.3
%description -n python3-%{pypi_name}
A Python interface to Aliyun Web Services


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
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu May 28 2020 mockbuilder - 1.20.0-1
- Initial package.