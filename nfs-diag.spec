%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name: nfs-diag
Version: 1.0
Release: 1%{?dist}

Summary: Looks for nfs mount points and collects diagnostics data, including a tcpdump.
Source0: %{name}-%{version}.tar.gz
License: GPLv2
Group: Developement/Libaries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch
BuildRequires: python-devel >= 2.5 python-setuptools
Requires: python >= 2.5

%description
   Script finds NFS servers to run tcpdump on. By default the script runs in
   manual mode allowing the user to select which server the user would like
   to run on. All output of script will be archived and stored in users current
   directory.
%prep
%setup -q

%build
%{__python} setup.py build

%install
%{__rm} -rf ${RPM_BUILD_ROOT}
%{__python}  setup.py install --optimize 1 --root=${RPM_BUILD_ROOT}

%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
#%doc LICENSE AUTHORS PKG-INFO CHANGELOG
#%doc doc/*
%{_bindir}/*
%{python_sitelib}/*

%define __prelink_undo_cmd /bin/cat prelink library

