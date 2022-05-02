%define light_apps          icewm icesh icewmbg icewmhint icewm-session icewmtray
%define default_apps        %{light_apps} icehelp]

Name:		icewm
Summary:	X11 Window Manager
Version:	2.9.7
Release:	1
License:	LGPL
Group:		Graphical desktop/Icewm

URL:		https://github.com/ice-wm/icewm
Source0:	https://github.com/ice-wm/icewm/releases/download/%{version}/icewm-%{version}.tar.lz
Source2:	themes.tar.lzma
Source5:	icewm-16.png
Source6:	icewm-32.png
Source7:	icewm-48.png
Source8:	icewm-starticewm
Source9:	icewm-monochrome.tar.bz2
Source12:	icewm-menu-xdg
Source13:	xeditor.sh

# fix bindkey conflict xcin
Patch1:		icewm-1.2.26-xcin_bindy.patch
#Patch2:		icewm-1.2.13pre3-defaultfont.patch
Patch10:	icewm-desktop.patch
#Patch27:	icewm-1.6.4-fix-cmake-openmandriva.patch
BuildRequires:	cmake
BuildRequires:	lzip
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(fribidi)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  linuxdoc-tools
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(imlib2)
BuildRequires:	asciidoc
BuildRequires:	asciidoctor
BuildRequires:	perl-Pod-Html
Requires:	desktop-common-data
Requires:	%{name}-i18n >= %{EVRD}
Recommends:	%{name}-themes
Recommends:	xterm
Recommends:	udisks-glue
%rename %{name}-light

%description
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

%package themes
Summary:	Extra themes of Icewm
Group:		Graphical desktop/Icewm
BuildArch: 	noarch

%description themes
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is themes collection for icewm window manager.

%package i18n
Summary:	locale files of Icewm
Group:		Graphical desktop/Icewm
BuildArch: 	noarch

%description i18n
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is translation files for icewm window manager.

%prep
%autosetup -p1 -a 2 -a 9 -n %{name}-%{version}

rm -f po/en.* #- en is not a valid locale

chmod -R a+rX themes
find themes -type f | xargs chmod a-x

#fix build with clang for arm and i686, https://github.com/bbidulock/icewm/issues/340
sed -i 's|windowList\[0\]|windowList[0U]|'  src/icesh.cc

%build
sed -i 's/ IceWM.jpg//' lib/CMakeLists.txt

%cmake \
	-DCFGDIR="%{_sysconfdir}/%{name}" \
	-DENABLE_LTO:BOOL=ON

%make_build

%install
%make_install -C build

cp -a themes %{buildroot}%{_datadir}/%{name}

install -D -m755 %{SOURCE12} %{buildroot}%{_sysconfdir}/menu.d/%{name}

# icon
install -D -m644 %{SOURCE6} %{buildroot}%{_iconsdir}/%{name}.png
install -D -m644 %{SOURCE5} %{buildroot}%{_miconsdir}/%{name}.png
install -D -m644 %{SOURCE7} %{buildroot}%{_liconsdir}/%{name}.png

(cd %{buildroot}%{_datadir} ; find %{name}/themes ! -type d -printf "%{_datadir}/%%p\n") > theme.list
(cd %{buildroot}%{_datadir} ; find %{name}/themes -type d -printf "%%%%dir %{_datadir}/%%p\n") >> theme.list

install -m 755 %{SOURCE8} %{buildroot}%{_bindir}/starticewm
install -m 755 %{SOURCE13} %{buildroot}%{_bindir}/xeditor

# Dadou - Change default background color for distro color
perl -pi -e "s!# DesktopBackgroundColor=.*!DesktopBackgroundColor=\"\"!" %buildroot%{_datadir}/icewm/preferences

# Get rid of useless stuff
rm %{buildroot}%{_bindir}/icewm-set-gnomewm


# Broken, so disable for now. See more here: https://issues.openmandriva.org/show_bug.cgi?id=2552 (penguin)
rm -f %buildroot/%_datadir/xsessions/%name.desktop

%find_lang %{name}

%files
%license COPYING
%doc README.md AUTHORS TODO THANKS NEWS
%doc doc/icewm.adoc
%doc %{_docdir}/icewm/*
%{_bindir}/icesound
%{_bindir}/icesh
%{_bindir}/icehelp
%{_bindir}/icewm
%{_bindir}/icewm-menu-xrandr
%{_bindir}/icewm-session
%{_bindir}/icewmbg
%{_bindir}/icewmhint
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/icons
%dir %{_datadir}/%{name}/ledclock
%dir %{_datadir}/%{name}/taskbar
%dir %{_datadir}/%{name}/mailbox
%{_sysconfdir}/menu.d/%{name}
#{_datadir}/xsessions/%{name}.desktop
%{_datadir}/xsessions/%{name}-session.desktop
%{_bindir}/starticewm
%{_bindir}/icewm-menu-fdo
%{_bindir}/xeditor
%{_datadir}/%{name}/mailbox/*
%{_datadir}/%{name}/taskbar/*
%{_datadir}/%{name}/ledclock/*
%{_datadir}/%{name}/icons/*
%{_datadir}/%{name}/keys
%{_datadir}/%{name}/menu
%{_datadir}/%{name}/programs
%{_datadir}/%{name}/preferences
%{_datadir}/%{name}/toolbar
%{_datadir}/%{name}/winoptions
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man*/*

%files themes -f theme.list

%files i18n -f %{name}.lang
