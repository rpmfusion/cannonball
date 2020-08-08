# force out-of-tree build for spec compatibility with older releases
%undefine __cmake_in_source_build

Name:           cannonball
Version:        0.3
Release:        10%{?dist}
Summary:        An Enhanced OutRun Engine

License:        MAME
URL:            https://github.com/djyt/cannonball/wiki
Source0:        https://github.com/djyt/%{name}/archive/v0.3/%{name}-%{version}.tar.gz
# Launcher and README adapted from AUR package
# https://aur.archlinux.org/packages/cannonball/
Source1:        %{name}.sh
Source2:        %{name}_README.Fedora
# Cannonball icon by Joseph Wharton
# http://joeystitch.deviantart.com/art/Outrun-Icon-256x256-435538436
Source3:        %{name}.png
Source4:        %{name}.desktop
# Adapt XML Writer to new boost api
# Add missing include
# https://github.com/djyt/cannonball/pull/14
Patch0:         %{name}-0.3-fixes.patch

BuildRequires:  SDL-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Cannonball is a program which allows you to play an enhanced version of 
Yu Suzuki's seminal arcade racer, OutRun, on a variety of systems:
- 60 fps gameplay (smoother than the original game)
- True widescreen mode (extend the play area by 25%)
- High Resolution mode (improves sprite scaling)
- Time Trial Mode
- Cheats
- Customisable Music
- High Score Saving
- Western, Japanese & prototype track support
- Analog & Digital controllers supported
- Force Feedback / Haptic support (Windows only)
- Fixes bugs present in the original game


%prep
%autosetup -p1

# Fix path in CMakeLists.txt
sed -i 's!set(CMDIR ../cmake)!set(CMDIR ./cmake)!' cmake/CMakeLists.txt

# Do not link SDLmail
sed -i '/SDLmain/d' cmake/debian.cmake

# Fix boost path
sed -i 's!${lib_base}/boost_1_54_0!${lib_base}/boost!' \
  cmake/CMakeLists.txt


%build
%cmake ./cmake \
  -DTARGET=debian \
  -DCMAKE_SKIP_BUILD_RPATH=TRUE
%cmake_build


%install
# Install launcher and binary
mkdir -p  %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
install -p -m 755 %{_vpath_builddir}/%{name} %{buildroot}%{_libexecdir}/%{name}

# Install config
mkdir -p %{buildroot}%{_datadir}/%{name}
install -p -m 644 %{_vpath_builddir}/config.xml %{buildroot}%{_datadir}/%{name}/config.xml

# Install Fedora README
install -p -m 644 %{SOURCE2} README.Fedora

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE4}

# Install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -p -m 644 %{SOURCE3} \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png


%files
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%license docs/license.txt
%doc roms/roms.txt
%doc README.Fedora


%changelog
* Thu Aug 06 2020 Andrea Musuruane <musuruan@gmail.com> - 0.3-10
- Fixed FTBFS for F33
- Removed desktop scriptlets

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 11 2017 Andrea Musuruane <musuruan@gmail.com> - 0.3-3
- Fixed boost include path

* Tue Aug 08 2017 Andrea Musuruane <musuruan@gmail.com> - 0.3-2
- Updated Source URL
- Fixed License
- Added missing BuildRequires (desktop-file-utils)
- Added missing Requires (hicolor-icon-theme)
- Improved macro usage
- Preserved timestamps

* Sun Oct 18 2015 Andrea Musuruane <musuruan@gmail.com> - 0.3-1
- First release

