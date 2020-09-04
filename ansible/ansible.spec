# Note to maintainers: master, all fedora branches and epel8 can be merged.
# epel7 and epel6 should be updated seperately. 
# (epel6 because it is still on 2.6 forever due to python support, 
# epel7 due to it using python2).

# in Fedora and EPEL8 build with docs and tests by default
%global with_docs 1

# Disable tests on f29/f30 and epel8 for now. 
# epel8 is missing 2 required packages. 
# fedora29 and fedora30 have too old pytest
%if 0%{?fedora} < 31 || 0%{?rhel} >= 8
%global with_tests 0
%else
%global with_tests 1
%endif

Name: ansible
Summary: SSH-based configuration management, deployment, and task execution system
Version: 2.9.13
Release: 2%{?dist}

License: GPLv3+
Source0: https://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
Source1: ansible.attr
Source2: ansible-generator
Source3: macros.ansible
Url: http://ansible.com
BuildArch: noarch

# Disable failing test
Patch2: ansible-2.9.6-disable-test_build_requirement_from_path_no_version.patch
# Fix Python 3.9 compatibility
# Backported from upstream: https://github.com/ansible/ansible/pull/67891
Patch3: fix-python-3.9-compatibility.patch

# We used to have a ansible-python3 package that a number of other things
# started depending on, so we should now provide/obsolete it until they 
# can all adjust to just needing ansible.
Provides:      ansible-python3 = %{version}-%{release}
Obsoletes:     ansible-python3 < %{version}-%{release}

%if 0%{?with_tests}
#
# For tests
#
# These two exist on both fedora and rhel8
#
BuildRequires: python3-packaging
BuildRequires: python3-pexpect
#
# These only exist on Fedora. RHEL8 will just skip tests that need them.
#
%if 0%{?fedora}
BuildRequires: python3-paramiko
BuildRequires: python3-winrm

BuildRequires: python3-crypto
BuildRequires: python3-pbkdf2
BuildRequires: python3-httmock
BuildRequires: python3-gitlab
BuildRequires: python3-boto3
BuildRequires: python3-botocore
BuildRequires: python3-coverage
BuildRequires: python3-passlib
%endif
%endif
# For Docs/tests
BuildRequires: git-core
%if 0%{?with_docs}
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx-theme-alabaster
BuildRequires: python3-sphinx-notfound-page
BuildRequires: asciidoc
BuildRequires: python3-straight-plugin
%endif
BuildRequires: python3-devel
BuildRequires: python3-setuptools
# accelerate is the only thing that makes keyczar mandatory.  Since accelerate
# is deprecated, just ignore it
#BuildRequires: python-keyczar
BuildRequires: python3-six
BuildRequires: python3-nose
# We pin Pytest to version 4 for now
# as there are some test failures with
# version 5. See rhbz#1841968
BuildRequires: %{py3_dist pytest}
BuildRequires: python3-pytest-xdist
BuildRequires: python3-pytest-mock
BuildRequires: python3-requests
BuildRequires: python3-mock
BuildRequires: python3-jinja2
BuildRequires: python3-pyyaml
BuildRequires: python3-cryptography
BuildRequires: python3-pyvmomi

# RHEL8 doesn't have python3-paramiko or python3-winrm (yet), but Fedora does
Recommends: python3-paramiko
Recommends: python3-winrm
# accelerate is the only thing that makes keyczar mandatory.  Since accelerate
# is deprecated, just ignore it
#Requires: python3-keyczar
Requires: python3-setuptools
Requires: python3-six
Requires: python3-jinja2
Requires: python3-pyyaml
Requires: sshpass
# needed for json_query filter
Requires: python3-jmespath

%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

%package -n ansible-doc
Summary: Documentation for Ansible

%description -n ansible-doc

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package installs extensive documentation for ansible

%prep
%autosetup -p1
cp -a %{S:1} %{S:2} %{S:3} .

# this files will be provides by ansible_alicloud package
sed -i  's#, "ali_instance_info.py": \["ansible/modules/cloud/alicloud/_ali_instance_facts.py"\]##' SYMLINK_CACHE.json
rm lib/ansible/module_utils/alicloud_ecs.py
rm lib/ansible/modules/cloud/alicloud/__init__.py
rm lib/ansible/modules/cloud/alicloud/_ali_instance_facts.py
rm lib/ansible/modules/cloud/alicloud/ali_instance_info.py
rm lib/ansible/modules/cloud/alicloud/ali_instance.py
rm lib/ansible/plugins/doc_fragments/alicloud.py


%build

# Fix some files shebangs
sed -i -e 's|/usr/bin/env python|/usr/bin/python3|' test/lib/ansible_test/_data/*.py test/lib/ansible_test/_data/*/*.py test/lib/ansible_test/_data/*/*/*.py docs/bin/find-plugin-refs.py

# These we have to supress or the package will depend on /usr/bin/pwsh and not be installable.
sed -i -s 's|/usr/bin/env pwsh||' test/lib/ansible_test/_data/sanity/validate-modules/validate_modules/ps_argspec.ps1
sed -i -s 's|/usr/bin/env pwsh||' test/lib/ansible_test/_data/sanity/pslint/pslint.ps1
sed -i -s 's|/usr/bin/env pwsh||' test/lib/ansible_test/_data/requirements/sanity.ps1

# disable the python -s shbang flag as we want to be able to find non system modules
%global py3_shbang_opts %(echo %{py3_shbang_opts} | sed 's/-s//')
%py3_build

%if 0%{?with_docs}
  make PYTHON=/usr/bin/python3 SPHINXBUILD=sphinx-build-3 webdocs
%else
make PYTHON=/usr/bin/python3 -Cdocs/docsite config cli keywords modules plugins testing
%endif

%install
%py3_install

# Create system directories that Ansible defines as default locations in
# ansible/config/base.yml
DATADIR_LOCATIONS='%{_datadir}/ansible/collections
%{_datadir}/ansible/collections/ansible_collections
%{_datadir}/ansible/plugins/doc_fragments
%{_datadir}/ansible/plugins/action
%{_datadir}/ansible/plugins/become
%{_datadir}/ansible/plugins/cache
%{_datadir}/ansible/plugins/callback
%{_datadir}/ansible/plugins/cliconf
%{_datadir}/ansible/plugins/connection
%{_datadir}/ansible/plugins/filter
%{_datadir}/ansible/plugins/httpapi
%{_datadir}/ansible/plugins/inventory
%{_datadir}/ansible/plugins/lookup
%{_datadir}/ansible/plugins/modules
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/netconf
%{_datadir}/ansible/roles
%{_datadir}/ansible/plugins/strategy
%{_datadir}/ansible/plugins/terminal
%{_datadir}/ansible/plugins/test
%{_datadir}/ansible/plugins/vars'

UPSTREAM_DATADIR_LOCATIONS=$(grep -ri default lib/ansible/config/base.yml| tr ':' '\n' | grep '/usr/share/ansible')

if [ "$SYSTEM_LOCATIONS" != "$UPSTREAM_SYSTEM_LOCATIONS" ] ; then
	echo "The upstream Ansible datadir locations have changed.  Spec file needs to be updated"
	exit 1
fi

mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/plugins/
for location in $DATADIR_LOCATIONS ; do
	mkdir $RPM_BUILD_ROOT"$location"
done
mkdir -p $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/etc/ansible/roles/

cp examples/hosts $RPM_BUILD_ROOT/etc/ansible/
cp examples/ansible.cfg $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

cp -pr docs/docsite/rst .
%if 0%{?with_docs}
  cp -pr docs/docsite/_build/html %{_builddir}/%{name}-%{version}/html
%endif

install -Dpm0644 -t %{buildroot}%{_fileattrsdir} ansible.attr
install -Dpm0644 -t %{buildroot}%{_rpmmacrodir} macros.ansible
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} ansible-generator


%check
%if 0%{?with_tests}
ln -s /usr/bin/pytest-3 bin/pytest
pathfix.py -i %{__python3} -p test/lib/ansible_test/_data/cli/ansible_test_cli_stub.py
# This test needs a module not packaged in Fedora so disable it.
rm -f test/units/modules/cloud/cloudstack/test_cs_traffic_type.py
# These tests are failing with pytest 6
rm -f test/units/module_utils/facts/hardware/test_sunos_get_uptime_facts.py
rm -f test/units/modules/source_control/test_gitlab_runner.py
rm -f test/units/plugins/lookup/test_aws_secret.py
rm -f test/units/plugins/lookup/test_aws_ssm.py
make PYTHON=/usr/bin/python3 tests-py3
%endif

%files
%license COPYING
%doc README.rst PKG-INFO changelogs/CHANGELOG-v2.9.rst
%doc %{_mandir}/man1/ansible*
%config(noreplace) %{_sysconfdir}/ansible/
%{_bindir}/ansible*
%{_datadir}/ansible/
%{python3_sitelib}/ansible
%{python3_sitelib}/ansible_test
%{python3_sitelib}/*egg-info
%{_fileattrsdir}/ansible.attr
%{_rpmmacrodir}/macros.ansible
%{_rpmconfigdir}/ansible-generator

%files -n ansible-doc
%doc rst
%if 0%{?with_docs}
%doc html
%endif

%changelog
* Tue Sep 01 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.13-1
- Update to 2.9.13. Fixes CVE-2020-14365

* Tue Aug 11 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.12-1
- Update to 2.9.12.

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.11-4
- Add support for generating '>=' dependencies in RPM generator

* Sat Aug 08 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.11-3
- Add very basic support for generating dependencies in RPM generator

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.11-1
- Update to 2.9.11.

* Thu Jun 18 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.10-1
- Update to 2.9.10. 

* Fri May 29 2020 Charalampos Stratakis <cstratak@redhat.com> - 2.9.9-3
- Fix Python 3.9 compatibility (#1808674)
- Pin Pytest to version 4 for now

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9.9-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.9-1
- Update to 2.9.9. Fixes bug #1834582
- Fixes gathering facts on f32+ bug #1832625

* Sun Apr 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.7-3
- Own /usr/share/ansible/collections/ansible_collections

* Sun Apr 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.7-2
- Add macros for packaging Ansible collections

* Fri Apr 17 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.7-1
- Update to 2.9.7.
- fixes CVE-2020-1733 CVE-2020-1735 CVE-2020-1740 CVE-2020-1746 CVE-2020-1753 CVE-2020-10684 CVE-2020-10685 CVE-2020-10691
- Drop the -s from the shebang to allow ansible to use locally installed modules.

* Fri Mar 06 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.6-1
- Update to 2.9.6. Fixes bug #1810373
- fixes for CVE-2020-1737, CVE-2020-1739

* Thu Feb 13 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.5-1
- Update to 2.9.5. Fixes bug #1802725

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.4-1
- Update to 2.9.4 with one bugfix.

* Thu Jan 16 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.3-1
- Update to 2.9.3.

* Sun Dec 08 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.2-1
- Update to 2.9.2.

* Thu Nov 14 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.1-2
- Add Requires for python3-pyyaml

* Wed Nov 13 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.1-1
- Update to 2.9.1.

* Fri Nov 08 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.0-2
- Supress pwsh requires added by rpm.

* Thu Oct 31 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.0-1
- Update to 2.9.0.

* Thu Oct 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.6-1
- Update to 2.8.6.
- Rework spec file to drop old conditionals.

* Thu Oct 10 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.5-2
- Make python3-paramiko and python3-winrm Recommended so they install on Fedora and not RHEL8

* Fri Sep 13 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.5-1
- Update to 2.8.5.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.4-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.4-1
- Update to 2.8.4. Fixes CVE-2019-10217 and CVE-2019-10206

* Thu Jul 25 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.3-1
- Update to 2.8.3.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.2-1
- Update to 2.8.2. Fixes bug #1726846

* Sun Jun 09 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.1-1
- Update to 2.8.1. Fixes bug #1718131
- Sync up Requires/Buildrequires with upstream.
- Add patch for python 3.8 building. Fixes bug #1712531
- Add patch for CVE-2019-10156.

* Fri May 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-2
- Fixes for various releases build/test issues.

* Fri May 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-1
- Update to 2.8.0 final. 
- Add datadirs for other packages to land ansible files in.

* Fri May 10 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.4rc3
- Update to 2.8.0 rc3.

* Thu May 02 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.3rc2
- Update to 2.8.0 rc2.

* Fri Apr 26 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.2rc1
- Update to 2.8.0 rc1.

* Mon Apr 22 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.1b
- Update to 2.8.0 beta 1.

* Thu Apr 04 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.10-1
- Update to 2.7.10. Fixes bug #1696379

* Thu Mar 14 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.9-1
- Update to 2.7.9. Fixes bug #1688974

* Thu Feb 21 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.8-1
- Update to 2.7.8. Fixes bug #1679787
- Fix for CVE-2019-3828

* Thu Feb 07 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.7-1
- Update to 2.7.7. Fixes bug #1673761

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.6-1
- Update to 2.7.6.

* Thu Dec 13 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.5-1
- Update to 2.7.5

* Mon Dec 03 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.4-1
- Update to 2.7.4

* Thu Nov 29 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.3-1
- Update to 2.7.3

* Thu Nov 15 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.2-1
- Update to 2.7.2.

* Mon Oct 29 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.1-1
- Update to 2.7.1.

* Thu Oct 04 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.0-1
- Update to 2.7.0

* Fri Sep 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.5-1
- Update to 2.6.5.

* Fri Sep 07 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.4-1
- Update to 2.6.4.

* Thu Aug 16 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.3-1
- Upgrade to 2.6.3.

* Sat Jul 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.2-1
- Update to 2.6.2. Fixes bug #1609486

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.1-1
- Update to 2.6.1. Fixes bug #1598602
- Fixes CVE-2018-10874 and CVE-2018-10875

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.0-1
- Update to 2.6.0. Fixes bug #1596424

* Tue Jun 26 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-5
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.5.5-4
- Upstream patch to build docs with older jinja2 (Fedora 27)
- Build changes to build only rst docs for modules and plugins when a distro
  doesn't have modern enough packages to build the documentation. (EPEL7)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-3
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-2
- Stop building docs on F27 as python-jinja2 is too old there.

* Thu Jun 14 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-1
- Update to 2.5.5. Fixes bug #1580530 and #1584927
- Fixes 1588855,1590200 (fedora) and 1588855,1590199 (epel)
  CVE-2018-10855 (security bug with no_log handling)

* Thu May 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.4-1
- Update to 2.5.4. Fixes bug #1584927

* Thu May 17 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.3-1
- Update to 2.5.3. Fixes bug #1579577 and #1574221

* Thu Apr 26 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.2-1
- Update to 2.5.2 with bugfixes.

* Wed Apr 18 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.1-1
- Update to 2.5.1 with bugfixes. Fixes: #1569270 #1569153 #1566004 #1566001

* Tue Mar 27 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-2
- Some additional python3 fixes. Thanks churchyard!

* Sat Mar 24 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-1
- Update to 2.5.0. Fixes bug #1559852
- Spec changes/improvements with tests, docs, and conditionals.

* Fri Mar 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.3.0-3
- Don't build and ship Python 2 bits on EL > 7 and Fedora > 29

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.4.3.0-1
- Update to 2.4.3. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Jan 08 2018 Troy Dawson <tdawson@redhat.com> - 2.4.2.0-2
- Update conditional

* Wed Nov 29 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.2.0-1
- Update to 2.4.2. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Oct 30 2017 Kevin Fenzi kevin@scrye.com - 2.4.1.0-2
- Add PR to conditionalize docs building. Thanks tibbs!
- Fix up el6 patches

* Thu Oct 26 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.1.0-1
- Update to 2.4.1

* Thu Oct 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.4.0.0-3
- Fix Python3 subpackage to symlink to the python3 versions of the scripts
  instead of the python2 version

* Mon Sep 25 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-2
- Rebase rhel6 jinja2 patch.
- Conditionalize jmespath to work around amazon linux issues. Fixes bug #1494640

* Tue Sep 19 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-1
- Update to 2.4.0. 

* Tue Aug 08 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.2.0-1
- Update to 2.3.2. Fixes bugs #1471017 #1461116 #1465586

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.1.0-1
- Update to 2.3.1.0.

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-3
- Update backported patch to the one actually merged upstream

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-2
- Backport hotfix to fix ansible-galaxy regression https://github.com/ansible/ansible/issues/22572

* Wed Apr 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.0.0-1
- Update to 2.3.0
- Remove upstreamed patches
- Remove controlpersist socket path path as a custom solution was included
  upstream
- Run the unittests from the upstream tarball now instead of having to download
  separately
- Build a documentation subpackage

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-3
- Deal with RHEL7 pytest vs python-pytest.
- Rebase epel6 newer jinja patch.
- Conditionalize exclude for RHEL6 rpm.

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-2
- Conditionalize python3 files for epel builds.

* Tue Mar 28 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-1
- 2.2.2.0 final
- Add new patch to fix unittests

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.4.rc1
- Add python-crypto and python3-crypto as explicit requirements

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.3.rc1
- Add a symlink for ansible executables to be accessed via python major version
  (ie: ansible-3) in addition to python-major-minor (ansible-3.6)

* Wed Mar  8 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.2.rc1
- Add a python3 ansible package.  Note that upstream doesn't intend for the library
  to be used by third parties so this is really just for the executables.  It's not
  strictly required that the executables be built for both python2 and python3 but
  we do need to get testing of the python3 version to know if it's stable enough to
  go into the next Fedora.  We also want the python2 version available in case a user
  has to get something done and the python3 version is too buggy.
- Fix Ansible cli scripts to handle appended python version

* Wed Feb 22 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-0.1.rc1
- Update to 2.2.2.0 rc1. Fixes bug #1421485

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.1.0-1
- Update to 2.2.1.
- Fixes: CVE-2016-9587 CVE-2016-8647 CVE-2016-9587 CVE-2016-8647
- Fixes bug #1405110

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-3
- Update unit tests that will skip docker related tests if docker isn't available.
- Drop docker BuildRequires. Fixes bug #1392918

* Fri Nov  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.0.0-3
- Fix for dnf group install

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-2
- Fix some BuildRequires to work on all branches.

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-1
- Update to 2.2.0. Fixes #1390564 #1388531 #1387621 #1381538 #1388113 #1390646 #1388038 #1390650
- Fixes for CVE-2016-8628 CVE-2016-8614 CVE-2016-8628 CVE-2016-8614

* Thu Sep 29 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.2.0-1
- Update to 2.1.2

* Thu Jul 28 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.1.0-1
- Update to 2.1.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Matt Domsch <matt@domsch.com> - 2.1.0.0-2
- Force python 2.6 on EL6

* Wed May 25 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.0.0-1
- Update to 2.1.0.0.
- Fixes: 1334097 1337474 1332233 1336266

* Tue Apr 19 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.2.0-1
- Update to 2.0.2.0. https://github.com/ansible/ansible/blob/stable-2.0/CHANGELOG.md
- Fixes CVE-2016-3096
- Fix for failed to resolve remote temporary directory issue. bug #1328359

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-2
- Patch control_path to be not hit path length limitations (RH BZ #1311729)
- Version the test tarball

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-1
- Update to upstream bugfix for 2.0.x release series.

* Thu Feb  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-3
- Utilize the python-jinja26 package on EPEL6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-1
- Ansible 2.0.0.2 release from upstream.  (Minor bugfix to one callback plugin
  API).

* Tue Jan 12 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0.1-1
- Ansible 2.0.0.1 from upstream.  Rewrite with many bugfixes, rewritten code,
  and new features. See the upstream changelog for details:
  https://github.com/ansible/ansible/blob/devel/CHANGELOG.md

* Wed Oct 14 2015 Adam Williamson <awilliam@redhat.com> - 1.9.4-2
- backport upstream fix for GH #2043 (crash when pulling Docker images)

* Fri Oct 09 2015 Kevin Fenzi <kevin@scrye.com> 1.9.4-1
- Update to 1.9.4

* Sun Oct 04 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-3
- Backport dnf module from head. Fixes bug #1267018

* Tue Sep  8 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.3-2
- Pull in patch for yum module that fixes state=latest issue

* Thu Sep 03 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-1
- Update to 1.9.3
- Patch dnf as package manager. Fixes bug #1258080
- Fixes bug #1251392 (in 1.9.3 release)
- Add requires for sshpass package. Fixes bug #1258799

* Thu Jun 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.2-1
- Update to 1.9.2

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-2
- Fix for dnf

* Tue Apr 28 2015 Kevin Fenzi <kevin@scrye.com> 1.9.1-1
- Update to 1.9.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-2
- Drop upstreamed epel6 patches. 

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-1
- Update to 1.9.0.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0-1
- Update to 1.9.0

* Thu Feb 19 2015 Kevin Fenzi <kevin@scrye.com> 1.8.4-1
- Update to 1.8.4

* Tue Feb 17 2015 Kevin Fenzi <kevin@scrye.com> 1.8.3-1
- Update to 1.8.3

* Sun Jan 11 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.8.2-3
- Work around a bug in python2.6 by using simplejson (applies in EPEL6)

* Wed Dec 17 2014 Michael Scherer <misc@zarb.org> 1.8.2-2
- precreate /etc/ansible/roles and /usr/share/ansible_plugins

* Sun Dec 07 2014 Kevin Fenzi <kevin@scrye.com> 1.8.2-1
- Update to 1.8.2

* Thu Nov 27 2014 Kevin Fenzi <kevin@scrye.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-2
- Rebase el6 patch

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-1
- Update to 1.8

* Thu Oct  9 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.2-2
- Add /usr/bin/ansible to the rhel6 newer pycrypto patch

* Wed Sep 24 2014 Kevin Fenzi <kevin@scrye.com> 1.7.2-1
- Update to 1.7.2

* Thu Aug 14 2014 Kevin Fenzi <kevin@scrye.com> 1.7.1-1
- Update to 1.7.1

* Wed Aug 06 2014 Kevin Fenzi <kevin@scrye.com> 1.7-1
- Update to 1.7

* Fri Jul 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.10-1
- Update to 1.6.10

* Thu Jul 24 2014 Kevin Fenzi <kevin@scrye.com> 1.6.9-1
- Update to 1.6.9 with more shell quoting fixes.

* Tue Jul 22 2014 Kevin Fenzi <kevin@scrye.com> 1.6.8-1
- Update to 1.6.8 with fixes for shell quoting from previous release. 
- Fixes bugs #1122060 #1122061 #1122062

* Mon Jul 21 2014 Kevin Fenzi <kevin@scrye.com> 1.6.7-1
- Update to 1.6.7
- Fixes CVE-2014-4966 and CVE-2014-4967

* Tue Jul 01 2014 Kevin Fenzi <kevin@scrye.com> 1.6.6-1
- Update to 1.6.6

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.5-1
- Update to 1.6.5

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.4-1
- Update to 1.6.4

* Mon Jun 09 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-1
- Update to 1.6.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 1.6.2-1
- Update to 1.6.2 release

* Wed May  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.1-1
- Bugfix 1.6.1 release

* Mon May  5 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6-1
- Update to 1.6
- Drop accelerate fix, merged upstream
- Refresh RHEL6 pycrypto patch.  It was half-merged upstream.

* Fri Apr 18 2014 Kevin Fenzi <kevin@scrye.com> 1.5.5-1
- Update to 1.5.5

* Mon Apr  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-2
- Fix setuptools requirement to apply to rhel=6, not rhel<6

* Wed Apr  2 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4
- Add upstream patch to fix accelerator mode
- Merge fedora and el6 spec files

* Fri Mar 14 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-2
- Update to NEW 1.5.3 upstream release.
- Add missing dependency on python-setuptools (el6 build)

* Thu Mar 13 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-1
- Update to 1.5.3
- Fix ansible-vault for newer python-crypto dependency (el6 build)

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-2
- Update to redone 1.5.2 release

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-1
- Update to 1.5.2

* Mon Mar 10 2014 Kevin Fenzi <kevin@scrye.com> 1.5.1-1
- Update to 1.5.1

* Fri Feb 28 2014 Kevin Fenzi <kevin@scrye.com> 1.5-1
- Update to 1.5

* Wed Feb 12 2014 Kevin Fenzi <kevin@scrye.com> 1.4.5-1
- Update to 1.4.5

* Sat Dec 28 2013 Kevin Fenzi <kevin@scrye.com> 1.4.3-1
- Update to 1.4.3 with ansible galaxy commands.
- Adds python-httplib2 to requires

* Wed Nov 27 2013 Kevin Fenzi <kevin@scrye.com> 1.4.1-1
- Update to upstream 1.4.1 bugfix release

* Thu Nov 21 2013 Kevin Fenzi <kevin@scrye.com> 1.4-1
- Update to 1.4

* Tue Oct 29 2013 Kevin Fenzi <kevin@scrye.com> 1.3.4-1
- Update to 1.3.4

* Tue Oct 08 2013 Kevin Fenzi <kevin@scrye.com> 1.3.3-1
- Update to 1.3.3

* Thu Sep 19 2013 Kevin Fenzi <kevin@scrye.com> 1.3.2-1
- Update to 1.3.2 with minor upstream fixes

* Mon Sep 16 2013 Kevin Fenzi <kevin@scrye.com> 1.3.1-1
- Update to 1.3.1

* Sat Sep 14 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-2
- Merge upstream spec changes to support EPEL5
- (Still needs python26-keyczar and deps added to EPEL)

* Thu Sep 12 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-1
- Update to 1.3.0
- Drop node-fireball subpackage entirely.
- Obsolete/provide fireball subpackage. 
- Add Requires python-keyczar on main package for accelerated mode.

* Wed Aug 21 2013 Kevin Fenzi <kevin@scrye.com> 1.2.3-2
- Update to 1.2.3
- Fixes CVE-2013-4260 and CVE-2013-4259

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Kevin Fenzi <kevin@scrye.com> 1.2.2-1
- Update to 1.2.2 with minor fixes

* Fri Jul 05 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-2
- Update to newer upstream re-release to fix a syntax error

* Thu Jul 04 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-1
- Update to 1.2.1
- Fixes CVE-2013-2233

* Mon Jun 10 2013 Kevin Fenzi <kevin@scrye.com> 1.2-1
- Update to 1.2

* Tue Apr 02 2013 Kevin Fenzi <kevin@scrye.com> 1.1-1
- Update to 1.1

* Mon Mar 18 2013 Kevin Fenzi <kevin@scrye.com> 1.0-1
- Update to 1.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.9-0
- Release 0.9

* Fri Oct 19 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.8-0
- Release of 0.8

* Thu Aug 9 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.7-0
- Release of 0.7

* Mon Aug 6 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.6-0
- Release of 0.6

* Wed Jul 4 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.5-0
- Release of 0.5

* Wed May 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.4-0
- Release of 0.4

* Mon Apr 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.3-1
- Release of 0.3

* Tue Apr  3 2012 John Eckersberg <jeckersb@redhat.com> - 0.0.2-1
- Release of 0.0.2

* Sat Mar 10 2012  <tbielawa@redhat.com> - 0.0.1-1
- Release of 0.0.1
