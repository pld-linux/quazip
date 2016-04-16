#
# Conditional build:
%bcond_without	qt4		# Qt 4 version
%bcond_without	qt5		# Qt 5 version

Summary:	Qt/C++ wrapper for the minizip library
Summary(pl.UTF-8):	Obudowanie Qt/C++ do biblioteki minizip
Name:		quazip
Version:	0.7.2
Release:	2
License:	GPL v2+ or LGPL v2+
Group:		X11/Libraries
Source0:	http://downloads.sourceforge.net/quazip/%{name}-%{version}.tar.gz
# Source0-md5:	84163487a4c3470781c93e5f56c4ca43
URL:		http://quazip.sourceforge.net/
BuildRequires:	cmake >= 2.6
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	libstdc++-devel
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

%description devel
This package contains the header files and documentation for
developing applications that use QuaZIP with Qt 4.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz dokumentację do tworzenia
aplikacji wykorzystujących QuaZIP wraz z Qt 4.

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

%description qt5-devel
This package contains the header files and documentation for
developing applications that use QuaZIP with Qt 5.

%description qt5-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz dokumentację do tworzenia
aplikacji wykorzystujących QuaZIP wraz z Qt 5.

%prep
%setup -q

%build
install -d build-qt{4,5}
%if %{with qt4}
cd build-qt4
export CXXFLAGS="%{rpmcxxflags} -fPIC"
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	..
%{__make}
cd ..
%endif

%if %{with qt5}
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
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif
%if %{with qt5}
%{__make} -C build-qt5 install/fast \
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
%attr(755,root,root) %ghost %{_libdir}/libquazip.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/html
%attr(755,root,root) %{_libdir}/libquazip.so
%{_includedir}/quazip
%{_datadir}/cmake/Modules/FindQuaZip.cmake
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%doc COPYING NEWS.txt README.txt
%attr(755,root,root) %{_libdir}/libquazip5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquazip5.so.1

%files qt5-devel
%defattr(644,root,root,755)
%doc doc/html
%attr(755,root,root) %{_libdir}/libquazip5.so
%{_includedir}/quazip5
%{_datadir}/cmake/Modules/FindQuaZip5.cmake
%endif
