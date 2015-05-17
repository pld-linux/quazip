#
# Conditional build:
%bcond_without	qt4		# build Qt4
%bcond_without	qt5		# build Qt5

Summary:	Qt/C++ wrapper for the minizip library
Name:		quazip
Version:	0.7.1
Release:	1
License:	GPLv2+ or LGPLv2+
Group:		X11/Libraries
Source0:	http://downloads.sourceforge.net/quazip/%{name}-%{version}.tar.gz
# Source0-md5:	3b99effb2a9417707d463e6f19cf2629
Patch1:		qt5.patch
URL:		http://quazip.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
%if %{with qt4}
BuildRequires:	qt4-build
%endif
%if %{with qt5}
BuildRequires:	qt5-build
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package
that can be used to access ZIP archives. It uses Trolltech's Qt
toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice
API, and - yes! - that means that you can also use QTextStream,
QDataStream or whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both
reading from and writing to ZIP archives.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries, header files and
documentation for developing applications that use %{name}.

%package qt5
Summary:	Qt/C++ wrapper for the minizip library
Group:		X11/Libraries

%description qt5
QuaZIP is a simple C++ wrapper over Gilles Vollant's ZIP/UNZIP package
that can be used to access ZIP archives. It uses Trolltech's Qt
toolkit.

QuaZIP allows you to access files inside ZIP archives using QIODevice
API, and - yes! - that means that you can also use QTextStream,
QDataStream or whatever you would like to use on your zipped files.

QuaZIP provides complete abstraction of the ZIP/UNZIP API, for both
reading from and writing to ZIP archives.

%package qt5-devel
Summary:	Development files for %{name}
Summary:	Qt5 wrapper for the minizip library
Group:		Development/Libraries
Requires:	%{name}-qt5 = %{version}-%{release}

%description qt5-devel
The %{name}-devel package contains libraries, header files and
documentation for developing applications that use %{name}.

%prep
%setup -q
%patch1 -p1

%build
install -d build-qt{4,5}
%if %{with qt4}
cd build-qt4
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	..
%{__make}
cd ..
%endif

%if %{with qt4}
cd build-qt5
%cmake \
	-DBUILD_WITH_QT4:BOOL=OFF \
	..
%{__make}
cd ..
%endif

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
%{__make} -C build-qt5 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif
%if %{with qt5}
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc COPYING NEWS.txt README.txt
%attr(755,root,root) %{_libdir}/libquazip.so.*.*.*
%ghost %{_libdir}/libquazip.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/html
%{_libdir}/libquazip.so
%{_includedir}/quazip
%{_datadir}/cmake/Modules/FindQuaZip.cmake
%endif

%if %{with qt4}
%files qt5
%defattr(644,root,root,755)
%doc COPYING NEWS.txt README.txt
%attr(755,root,root) %{_libdir}/libquazip5.so.*.*.*
%ghost %{_libdir}/libquazip5.so.1

%files qt5-devel
%defattr(644,root,root,755)
%doc doc/html
%{_libdir}/libquazip5.so
%{_includedir}/quazip5
%{_datadir}/cmake/Modules/FindQuaZip5.cmake
%endif
