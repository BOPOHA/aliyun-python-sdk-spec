# Created by pyp2rpm-3.3.2
%global pypi_name ansible_alicloud_module_utils

Name:           python-%{pypi_name}
Version:        1.5.0
Release:        2%{?dist}
Summary:        The dependence of Ansible Provider Alicloud modules

License:        MIT
URL:            None
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(ansible)
%if 0%{?fedora} >= 31
Requires:       python3dist(footmark) >= 1.20
%else
Requires:       python3dist(footmark) >= 1.20.0
%endif
%description -n python3-%{pypi_name}



%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%{python3_sitelib}/ansible
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Wed May 27 2020 mockbuilder - 1.5.0-1
- Initial package.