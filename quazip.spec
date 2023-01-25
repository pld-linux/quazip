#
# Conditional build:
%bcond_without	qt4		# Qt 4 version
%bcond_without	qt5		# Qt 5 version
%bcond_without	static_libs	# static libraries

Summary:	Qt/C++ wrapper for the minizip library
Summary(pl.UTF-8):	Obudowanie Qt/C++ do biblioteki minizip
Name:		quazip
Version:	1.3
Release:	1
License:	GPL v2+ or LGPL v2+
Group:		X11/Libraries
#Source0Download: https://github.com/stachenov/quazip/releases
Source0:	https://github.com/stachenov/quazip/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	52b45020f8153a45920cd572d777c6a7
Patch0:		cmake.patch
URL:		https://stachenov.github.io/quazip/
BuildRequires:	cmake >= 3.15
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	zlib-devel
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4.5.0
BuildRequires:	qt4-build >= 4.5.0
BuildRequires:	qt4-qmake >= 4.5.0
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%endif
Requires:	QtCore-devel >= 4.5.0
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

%description -l pl.UTF-8
QuaZIP to proste obudowanie C++ dla pakietu ZIP/UNZIP Gillesa
Vollanta, który może być używany do dostępu do archiwów ZIP. QuaZIP
wykorzystuje bibliotekę narzędziową Qt firmy Trolltech.

QuaZIP pozwala na dostęp do plików wewnątrz archiwów ZIP przy użyciu
API QIODevice, co oznacza, że można używać QTextStream, QDataStream,
jak i innych na zzipowanych plikach.

QuaZIP udostępnia pełną abstrakcję API ZIP/UNZIP, zarówno dla odczytu,
jak i zapisu plikówZIP.

%package devel
Summary:	Development files for QuaZIP (Qt 4 version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QuaZIP (wersja dla Qt 4)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4.5.0
Requires:	zlib-devel

%description devel
This package contains the header files and documentation for
developing applications that use QuaZIP with Qt 4.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz dokumentację do tworzenia
aplikacji wykorzystujących QuaZIP wraz z Qt 4.

%package static
Summary:	Static QuaZIP library (Qt 4 version)
Summary(pl.UTF-8):	Statyczna biblioteka QuaZIP (wersja dla Qt 4)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static QuaZIP library (Qt 4 version).

%description static -l pl.UTF-8
Statyczna biblioteka QuaZIP (wersja dla Qt 4).

%package qt5
Summary:	Qt 5/C++ wrapper for the minizip library
Summary(pl.UTF-8):	Obudowanie Qt 5/C++ do biblioteki minizip
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

%description qt5 -l pl.UTF-8
QuaZIP to proste obudowanie C++ dla pakietu ZIP/UNZIP Gillesa
Vollanta, który może być używany do dostępu do archiwów ZIP. QuaZIP
wykorzystuje bibliotekę narzędziową Qt firmy Trolltech.

QuaZIP pozwala na dostęp do plików wewnątrz archiwów ZIP przy użyciu
API QIODevice, co oznacza, że można używać QTextStream, QDataStream,
jak i innych na zzipowanych plikach.

QuaZIP udostępnia pełną abstrakcję API ZIP/UNZIP, zarówno dla odczytu,
jak i zapisu plikówZIP.

%package qt5-devel
Summary:	Development files for QuaZIP (Qt 5 version)
Summary(pl.UTF-8):	Pliki programistyczne biblioteki QuaZIP (wersja dla Qt 5)
Group:		Development/Libraries
Requires:	%{name}-qt5 = %{version}-%{release}
Requires:	Qt5Core-devel >= 5
Requires:	zlib-devel

%description qt5-devel
This package contains the header files and documentation for
developing applications that use QuaZIP with Qt 5.

%description qt5-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz dokumentację do tworzenia
aplikacji wykorzystujących QuaZIP wraz z Qt 5.

%package qt5-static
Summary:	Static QuaZIP library (Qt 5 version)
Summary(pl.UTF-8):	Statyczna biblioteka QuaZIP (wersja dla Qt 5)
Group:		Development/Libraries
Requires:	%{name}-qt5-devel = %{version}-%{release}

%description qt5-static
Static QuaZIP library (Qt 5 version).

%description qt5-static -l pl.UTF-8
Statyczna biblioteka QuaZIP (wersja dla Qt 5).

%package apidocs
Summary:	API documentation for QuaZIP libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek QuaZIP
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for QuaZIP libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek QuaZIP.

%prep
%setup -q
%patch0 -p1

%build
export CXXFLAGS="%{rpmcxxflags} -fPIC"
%if %{with qt4}
%cmake -B build-qt4 \
	-DQUAZIP_QT_MAJOR_VERSION=4

%{__make} -C build-qt4

%if %{with static_libs}
%cmake -B build-qt4-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DQUAZIP_QT_MAJOR_VERSION=4

%{__make} -C build-qt4-static
%endif
%endif

%if %{with qt5}
%cmake -B build-qt5 \
	-DQUAZIP_QT_MAJOR_VERSION=5

%{__make} -C build-qt5

%if %{with static_libs}
%cmake -B build-qt5-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DQUAZIP_QT_MAJOR_VERSION=5

%{__make} -C build-qt5-static
%endif
%endif

doxygen Doxyfile
for file in doc/html/*; do
	touch -r Doxyfile $file
done

%install
rm -rf $RPM_BUILD_ROOT

%if %{with qt4}
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-qt4-static install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif
%endif

%if %{with qt5}
%{__make} -C build-qt5 install/fast \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-qt5-static install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif
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
%doc COPYING NEWS.txt README.md
%attr(755,root,root) %{_libdir}/libquazip1-qt4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquazip1-qt4.so.1.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquazip1-qt4.so
%{_includedir}/QuaZip-Qt4-1.3
%{_libdir}/cmake/QuaZip-Qt4-1.3
%{_pkgconfigdir}/quazip1-qt4.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libquazip1-qt4.a
%endif
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%doc COPYING NEWS.txt README.md
%attr(755,root,root) %{_libdir}/libquazip1-qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquazip1-qt5.so.1.3

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquazip1-qt5.so
%{_includedir}/QuaZip-Qt5-1.3
%{_libdir}/cmake/QuaZip-Qt5-1.3
%{_pkgconfigdir}/quazip1-qt5.pc

%if %{with static_libs}
%files qt5-static
%defattr(644,root,root,755)
%{_libdir}/libquazip1-qt5.a
%endif
%endif

%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*.{css,html,js,png}
