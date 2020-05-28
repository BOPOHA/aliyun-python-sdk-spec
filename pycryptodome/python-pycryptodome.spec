# Created by pyp2rpm-3.3.2
%global pypi_name pycryptodome

Name:           python-%{pypi_name}
Version:        3.9.7
Release:        1%{?dist}
Summary:        Cryptographic library for Python

License:        BSD, Public Domain, Apache
URL:            https://www.pycryptodome.org
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
 
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
PyCryptodome PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.It supports Python 2.6 and 2.7, Python 3.4 and newer,
and PyPy.You can install it with:: pip install pycryptodomeAll modules are
installed under the Crypto package.Check the pycryptodomex_ project for the
equivalent library that works under the Cryptodome package.PyCryptodome is a
fork of...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
PyCryptodome PyCryptodome is a self-contained Python package of low-level
cryptographic primitives.It supports Python 2.6 and 2.7, Python 3.4 and newer,
and PyPy.You can install it with:: pip install pycryptodomeAll modules are
installed under the Crypto package.Check the pycryptodomex_ project for the
equivalent library that works under the Cryptodome package.PyCryptodome is a
fork of...


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
%license Doc/LEGAL/copy/LICENSE.libtom Doc/LEGAL/copy/LICENSE.orig Doc/LEGAL/copy/LICENSE.python-2.2 Doc/ocb/license1.pdf Doc/ocb/license2.pdf Doc/ocb/license3.pdf Doc/src/license.rst LICENSE.rst
%doc Doc/ocb/README.txt README.rst lib/Crypto/SelfTest/Cipher/test_vectors/AES/README.txt lib/Crypto/SelfTest/Cipher/test_vectors/TDES/README.txt lib/Crypto/SelfTest/Hash/test_vectors/keccak/readme.txt lib/Crypto/SelfTest/Signature/test_vectors/ECDSA/README.txt
%{python3_sitearch}/Crypto
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu May 28 2020 mockbuilder - 3.9.7-1
- Initial package.