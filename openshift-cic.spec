%global pkgname openshift-cic
%global pypiname openshift_cic

Name:           %{pkgname)
Version:        1.0.0
Release:        1%{?dist}
Summary:        CNS Inventory file Creator (CIC)

License:        GPLv 3.0
URL:            https://github.com/red-hat-storage/openshift-cic
Source0:        https://github.com/ramkrsna/red-hat-storage/archive/master.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-setuptools
Requires:       python-jinja2

%description
Script which the user runs and then answers a list of questions to create
set of inventory_file options to be incorporated into their larger
inventory_file for running openshift-ansible playbooks. The goal is to
reduce the complexity and error prone nature of needing to know the
correct CNS/CRS inventory_file options for a particular OCP/CNS version.
The first prototype will be created for OCP 3.9 with the goal of
using with OCP 3.10 as well.

%prep
%autosetup -n %{pypiname}-%{version}

%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
%license LICENSE
%doc README MANIFEST.in
%{python_sitelib}/%{pypiname}/*
%{python_sitelib}/%{pypiname}-*.egg-info
%{_bindir}/cic

%changelog
* Mon Sep 17 2018 Ramakrishna Reddy Yekulla <rreddy@redhat.com> 0.0.1-1
- Added initial spec file
