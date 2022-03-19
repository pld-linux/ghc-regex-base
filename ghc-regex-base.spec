#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	regex-base
Summary:	Interface API for regex-posix,pcre,parsec,tdfa,dfa
Summary(pl.UTF-8):	API interfejsu dla regex-posix,pcre,parsec,tdfa,dfa
Name:		ghc-%{pkgname}
Version:	0.94.0.0
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/regex-base
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	91f7a3e19e419fb048b8babfecc1294b
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/regex-base
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 3.0
BuildRequires:	ghc-bytestring
BuildRequires:	ghc-containers
BuildRequires:	ghc-mtl
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 3.0
BuildRequires:	ghc-bytestring-prof
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-mtl-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 3.0
Requires:	ghc-bytestring
Requires:	ghc-containers
Requires:	ghc-mtl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Interface API for regex-posix,pcre,parsec,tdfa,dfa.

%description -l pl.UTF-8
API interfejsu dla regex-posix,pcre,parsec,tdfa,dfa.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 3.0
Requires:	ghc-bytestring-prof
Requires:	ghc-containers-prof
Requires:	ghc-mtl-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-base-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-base-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-base-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Base
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Base/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Base/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSregex-base-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Regex/Base/*.p_hi

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
