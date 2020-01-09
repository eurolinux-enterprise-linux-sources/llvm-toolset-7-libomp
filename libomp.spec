%{?scl:%scl_package libomp}
%{!?scl:%global pkg_name %{name}}

Name: %{?scl_prefix}libomp
Version: 5.0.1
Release: 2%{?dist}
Summary: OpenMP runtime for clang

License: NCSA
URL: http://openmp.llvm.org	
Source0: http://llvm.org/releases/%{version}/openmp-%{version}.src.tar.xz

Patch0: 0001-CMake-Make-LIBOMP_HEADERS_INSTALL_PATH-a-cache-varia.patch

BuildRequires: %{?scl_prefix}cmake
BuildRequires: elfutils-libelf-devel
BuildRequires: perl
BuildRequires: perl-Data-Dumper
BuildRequires: perl-Encode

Requires: elfutils-libelf

# libomp does not support s390x.
ExcludeArch: s390x

%description
OpenMP runtime for clang.

%package devel
Summary: OpenMP header files

%description devel
OpenMP header files.

%prep
%autosetup -n openmp-%{version}.src -p1

%build
mkdir -p _build
cd _build

# Use the scl-provided cmake instead of /usr/bin/cmake
%global __cmake %{_bindir}/cmake

%cmake .. \
	-DLIBOMP_INSTALL_ALIASES=OFF \
	-DLIBOMP_HEADERS_INSTALL_PATH:PATH=%{_libdir}/clang/%{version}/include \
%if 0%{?__isa_bits} == 64
	-DLIBOMP_LIBDIR_SUFFIX=64 \
%else
	-DLIBOMP_LIBDIR_SUFFIX= \
%endif

%make_build


%install
cd _build
%make_install


%files
%{_libdir}/libomp.so

%files devel
%{_libdir}/clang/%{version}/include/omp.h

%changelog
* Mon Jan 15 2018 Tom Stellard <tstellar@redhat.com> - 5.0.1-2
- Rebuild to include i686

* Thu Dec 21 2017 Tom Stellard <tstellar@redhat.com> - 5.0.1-1
- 5.0.1 Release.

* Wed Jun 21 2017 Tom Stellard <tstellar@redhat.com> - 4.0.1-1
- 4.0.1 Release.

* Wed Jun 07 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-3
- Rename libopenmp->libomp

* Fri May 26 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-2
- Disable build on s390x

* Mon May 15 2017 Tom Stellard <tstellar@redhat.com> - 4.0.0-1
- Initial version.
