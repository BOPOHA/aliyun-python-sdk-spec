# Created by pyp2rpm-3.3.2
%global pypi_name crcmod

Name:           python-%{pypi_name}
Version:        1.7
Release:        1%{?dist}
Summary:        CRC Generator

License:        MIT
URL:            http://crcmod.sourceforge.net/
Source0:        https://files.pythonhosted.org/packages/source/c/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)

%description
 crcmod for Calculating CRCs The software in this package is a Python module
for generating objects that compute the Cyclic Redundancy Check (CRC). There is
no attempt in this package to explain how the CRC works. There are a number of
resources on the web that give a good explanation of the algorithms. Just do a
Google search for "crc calculation" and browse till you find what you need....

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
 crcmod for Calculating CRCs The software in this package is a Python module
for generating objects that compute the Cyclic Redundancy Check (CRC). There is
no attempt in this package to explain how the CRC works. There are a number of
resources on the web that give a good explanation of the algorithms. Just do a
Google search for "crc calculation" and browse till you find what you need....

%package -n python-%{pypi_name}-doc
Summary:        crcmod documentation
%description -n python-%{pypi_name}-doc
Documentation for crcmod

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build
# generate html docs 
PYTHONPATH=${PWD} sphinx-build-3 docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%changelog
* Thu May 28 2020 mockbuilder - 1.7-1
- Initial package.