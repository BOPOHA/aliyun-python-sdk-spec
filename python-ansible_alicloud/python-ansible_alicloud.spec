# Created by pyp2rpm-3.3.2
%global pypi_name ansible_alicloud
# Turn off the brp-python-bytecompile automagic
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:           python-%{pypi_name}
Version:        1.19.0
Release:        8%{?dist}
Summary:        Ansible provider for Alicloud

License:        MIT
URL:            https://github.com/alibaba/ansible-provider/tree/master/lib/ansible
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
sed -i /install_requires=/d setup.py
rm lib/ansible/module_utils/__init__.py
rm lib/ansible/module_utils/alicloud_ecs.py
rm lib/ansible/modules/cloud/alicloud/_ali_instance_facts.py
rm lib/ansible/modules/cloud/alicloud/ali_instance_info.py
rm lib/ansible/modules/cloud/alicloud/ali_instance.py
rm lib/ansible/modules/cloud/__init__.py

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/ansible
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%exclude %{python3_sitelib}/ansible/__pycache__
%exclude %{python3_sitelib}/ansible/modules/__pycache__
%exclude %{python3_sitelib}/ansible/modules/cloud/alicloud/__pycache__
%exclude %{python3_sitelib}/ansible/utils/__pycache__

%changelog
* Wed May 27 2020 mockbuilder - 1.19.0-1
- Initial package.