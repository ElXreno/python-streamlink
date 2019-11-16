%{?python_enable_dependency_generator}

%global srcname streamlink
%global common_description Streamlink is a command-line utility that pipes video streams from various\
services into a video player, such as VLC. The main purpose of Streamlink is to\
allow the user to avoid buggy and CPU heavy flash plugins but still be able to\
enjoy various streamed content. There is also an API available for developers\
who want access to the video stream data. This project was forked from\
Livestreamer, which is no longer maintained.

# TODO: re-enable tests when python-freezegun >= 0.3.10 is available in
# repositories
%global _with_tests 0%{?fedora} >= 30

Name:           python-%{srcname}
Version:        1.2.0
Release:        2%{?dist}
Summary:        Python library for extracting streams from various websites

# src/streamlink/packages/requests_file.py is ASL 2.0
# src/streamlink/packages/flashmedia/ is MIT
License:        BSD and ASL 2.0 and MIT
URL:            https://streamlink.github.io/
Source0:        %{srcname}-%{version}-without-win32-binaries.tar.gz
# streamlink tarball contains FFmpeg and rtmpdump binaries for Windows which
# cannot be uploaded on Fedora servers for legal reasons. Therefore we use
# this script to download the tarball and remove forbidden files
Source1:        %{name}-generate-tarball.sh
# Fix requests version to the latest one available in Fedora
Patch0:         %{name}-1.0.0-dependencies.patch
# Fix PlayTV plugin (see https://github.com/streamlink/streamlink/pull/2388)
Patch1:         %{name}-1.1.1-playtv.patch
# Use pycryptodomex library instead of crypto
Patch2:         %{name}-1.2.0-pycryptodomex.patch

BuildRequires:  fontpackages-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Needed for documentation
BuildRequires:  python3-iso-639
BuildRequires:  python3-iso3166
BuildRequires:  python3-isodate
BuildRequires:  python3-jwt
BuildRequires:  python3-pycryptodomex
BuildRequires:  python3-recommonmark
BuildRequires:  python3-sphinx
BuildRequires:  python3-websocket-client
# Needed for tests
%if 0%{?_with_tests}
BuildRequires:  python3-freezegun
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  python3-requests-mock
%endif
BuildArch:      noarch

%description
%{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}
Provides:       %{srcname} = %{version}-%{release}

%description -n python3-%{srcname}
%{common_description}


%package doc
Summary:        Documentation for %{name}
Requires:       fontawesome-fonts-web

%description doc
%{common_description}

This package provides documentation for %{name}.


%prep
%autosetup -n %{srcname}-%{version} -p1

# Remove shebang
for i in $(find src/%{srcname}/ -name "*.py"); do
    sed '1{\@^#!/usr/bin/env python@d}' $i >$i.new && \
    touch -r $i $i.new && \
    mv $i.new $i
done


%build
%py3_build

# Generate documentation
%{__python3} setup.py build_sphinx -b man
%{__python3} setup.py build_sphinx -b html
rm build/sphinx/html/.buildinfo

# Drop bundled web fonts in HTML documentation
pushd build/sphinx/html/_static/fonts/
rm *
ln -s %{_fontbasedir}/fontawesome/fontawesome-webfont.eot .
popd


%install
%py3_install

# Install man page
install -Dpm 0644 build/sphinx/man/%{srcname}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{srcname}.1


%check
%if 0%{?_with_tests}
%{__python3} setup.py test
%endif


%files -n python3-%{srcname}
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md README.md
%license LICENSE NOTICE
%{_bindir}/%{srcname}
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}_cli/
%{_mandir}/man1/%{srcname}.1.*


%files doc
%doc build/sphinx/html/
%license LICENSE


%changelog
* Tue Aug 20 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- Use pycryptodomex library instead of crypto

* Wed Apr 03 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sun Mar 31 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14.2-5
- Enable python dependency generator

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.14.2-4
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.2-2
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.14.2-1
- Update to 0.14.2

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-2
- Rebuilt for Python 3.7

* Thu Jun 07 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.13.0-1
- Update to 0.13.0

* Mon May 07 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1

* Mon May 07 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Thu Mar 08 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.11.0-1
- Update to 0.11.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.10.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 24 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.10.0-1
- Update to 0.10.0

* Tue Nov 14 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Tue Oct 10 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.8.1-3
- Fix dependecy on python-websocket-client package

* Tue Sep 19 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.8.1-2
- Add missing dependecy on python-websocket-client package

* Tue Sep 19 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Thu May 11 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Wed Apr 05 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Fri Mar 10 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Wed Feb 22 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Sat Jan 07 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.0-3
- Add license to doc subpackage

* Sat Jan 07 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.0-2
- Fix license tag
- Move documentation to a subpackage
- Enable tests

* Sun Dec 18 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Fri Dec 16 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.0-1
- Initial RPM release
