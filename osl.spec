#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	OpenScop: Structures and formats for polyhedral tools to talk together
Summary(pl.UTF-8):	OpenScop - struktury i formaty do komunikacji między narzędziami wielościanowymi
Name:		osl
Version:	0.9.2
Release:	1
License:	BSD
Group:		Libraries
##Source0Download: http://icps.u-strasbg.fr/~bastoul/development/openscop/
#Source0:	http://icps.u-strasbg.fr/~bastoul/development/openscop/docs/%{name}-%{version}.tar.gz
#Source0Download: https://github.com/periscop/openscop/releases
Source0:	https://github.com/periscop/openscop/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	21b88885dd315da02b3b054c2ce1032e
Patch0:		%{name}-missing.patch
Patch1:		%{name}-info.patch
URL:		http://icps.u-strasbg.fr/~bastoul/development/openscop/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	libtool
BuildRequires:	rpm-pythonprov
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenScop is an open specification that defines a file format and a set
of data structures to represent a static control part (SCoP for
short), i.e., a program part that can be represented in the polyhedral
model. The goal of OpenScop is to provide a common interface to
various polyhedral compilation tools in order to simplify their
interaction. 

%description -l pl.UTF-8
OpenScop to otwarta specyfikacja definiująca formaty plików oraz zbiór
struktur danych do reprezentacji części sterowania statycznego (w
skrócie SCoP - Static Control Part), czyli części programu, która może
być reprezentowana w modelu wielościanowym. Celem biblioteki OpenScop
jest zapewnienie wspólnego interfejsu do różnych narzędzi
kompilujących opatych na wielościanach, aby uprościć ich interakcję.

%package devel
Summary:	Header files for OpenScop library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenScop
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel

%description devel
Header files for OpenScop library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenScop.

%package static
Summary:	Static OpenScop library
Summary(pl.UTF-8):	Statyczna biblioteka OpenScop
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenScop library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenScop.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README THANKS
%attr(755,root,root) %{_libdir}/libosl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosl.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libosl.so
%{_libdir}/libosl.la
%{_includedir}/osl
%dir %{_libdir}/osl
%{_libdir}/osl/osl-config.cmake
%{_infodir}/openscop.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/libosl.a
