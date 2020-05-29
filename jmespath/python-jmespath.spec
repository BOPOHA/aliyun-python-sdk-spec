# Created by pyp2rpm-3.3.2
%global pypi_name jmespath

Name:           python-%{pypi_name}
Version:        0.10.0
Release:        1%{?dist}
Summary:        JSON Matching Expressions

License:        MIT
URL:            https://github.com/jmespath/jmespath.py
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 JMESPath (pronounced "james path") allows you to declaratively specify how to
extract elements from a JSON document.For example, given this document::
{"foo": {"bar": "baz"}}The jmespath expression foo.bar will return "baz".

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
 JMESPath (pronounced "james path") allows you to declaratively specify how to
extract elements from a JSON document.For example, given this document::
{"foo": {"bar": "baz"}}The jmespath expression foo.bar will return "baz".


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%license LICENSE.txt
%doc README.rst
%{_bindir}/jp.py
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu May 28 2020 mockbuilder - 0.10.0-1
- Initial package.