# Created by pyp2rpm-3.3.5
%global pypi_name ansible_alicloud
# Turn off the brp-python-bytecompile automagic
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           python-%{pypi_name}
Version:        1.19.0
Release:        10%{?dist}
Summary:        Ansible provider for Alicloud

License:        MIT
URL:            https://github.com/alibaba/ansible-provider/tree/master/lib/ansible
Source0:        %{pypi_source}
# Patch1 contains 4 commits: 1cdc6d91201d8cf76e05dc7eca2a6f79454c7ae9, 6282147352879be72474cd7194ce5ddccf248677,
#                            66817356490ccf2cefbf8c64c16ea3301ffe2e41, 76f77264fa7a978b0a5fbad34139e15862b0048f
Patch1:         https://raw.githubusercontent.com/BOPOHA/aliyun-python-sdk-spec/develop/python-ansible_alicloud/279.merged.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(ansible)  == 2.9.15
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
sed -i /install_requires=/d setup.py
rm lib/ansible/module_utils/__init__.py
rm lib/ansible/modules/cloud/__init__.py

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/ansible
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/ansible/__pycache__
%exclude %{python3_sitelib}/ansible/modules/__pycache__
%exclude %{python3_sitelib}/ansible/modules/cloud/alicloud/__pycache__
%exclude %{python3_sitelib}/ansible/utils/__pycache__

%changelog
* Wed Nov 25 2020 Anatolii Vorona <vorona@alarstudios.com> - 1.19.0-10
- Update ansible up to 2.9.15. Added patch for ECS facts fix.

* Wed May 27 2020 mockbuilder - 1.19.0-1
- Initial package.
