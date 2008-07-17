Name:           vamp-plugin-sdk
Version:        1.3
Release:        1%{?dist}
Summary:        An API for audio analysis and feature extraction plugins

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.vamp-plugins.org/
Source0:        http://downloads.sourceforge.net/vamp/vamp-plugin-sdk-%{version}.tar.gz
Patch0:         %{name}-1.3-mk.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libsndfile-devel
#Requires:

%description
Vamp is an API for C and C++ plugins that process sampled audio data
to produce descriptive output (measurements or semantic observations).

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        static
Summary:        Static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description    static
The %{name}-static package contains library files for
developing static applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .mk


%build
CXXFLAGS=$RPM_OPT_FLAGS make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
# fix libdir
find . -name '*.pc.in' -exec sed -i 's|/lib|/%{_lib}|' {} ';'
make install DESTDIR=$RPM_BUILD_ROOT INSTALL_PREFIX=%{_prefix} LIB=/%{_lib}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# create Makefile for examples
cd examples
echo CXXFLAGS=$RPM_OPT_FLAGS -fpic >> Makefile
echo bundle: `ls *.o` >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -shared -Wl,-Bsymbolic \
     -o vamp-example-plugins.so \
     *.o \$\(pkg-config --libs vamp-sdk\) >> Makefile
echo `ls *.cpp`: >> Makefile
echo -e "\t"g++ \$\(CXXFLAGS\) -c $*.cpp >> Makefile
echo clean: >> Makefile
echo -e "\t"-rm *.o *.so >> Makefile
# clean directory up so we can package the sources
make clean


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc examples
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a


%changelog
* Thu Jul 17 2008 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.3-1
- Update to 1.3

* Thu Jan 31 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-4
- Add some #includes, needed due to GCC 4.3's header dependency cleanup

* Mon Jan 28 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-3
- Add examples to -devel subpackage
- Fix .pc files
- Preserve timestamps when installing

* Sun Jan 27 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-2
- Add missing build requirement on libsndfile-devel

* Wed Jan 16 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1b-1
- Initial Fedora package
