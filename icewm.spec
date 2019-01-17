%define light_apps          icewm icesh icewmbg icewmhint icewm-session icewmtray
%define default_apps        %{light_apps} icehelp

Name:		icewm
Summary:	X11 Window Manager
Epoch:		1
Version:	1.4.2
Release:	4
License:	LGPL
Group:		Graphical desktop/Icewm

URL:		https://github.com/bbidulock/icewm
Source0:	https://github.com/bbidulock/icewm/releases/download/%{version}/icewm-%{version}.tar.bz2
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
Patch2:		icewm-1.2.13pre3-defaultfont.patch
Patch4:		icewm-1.3-dev-winoptions.patch
Patch10:	icewm-desktop.patch
Patch12:	icewm-1.2.14pre11-background.patch
Patch25:	icewm-1.3.0-fix-focusing-on-raise.patch
Patch26:	icewm-1.4.2-mga-default-pref.patch
Patch27:	icewm-1.3.8-mga-fixdocdir.patch
Patch28:	icewm-1.3.12-build-taskbar-with-lite-build.patch
Patch29:	icewm-1.3.12-fix-light-with-taskbar-enabled.patch
BuildRequires:	autoconf2.5
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	libpcap-devel
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  linuxdoc-tools
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:	pkgconfig(xpm)
Requires:	desktop-common-data
Requires:	%{name}-light >= %{EVRD}
Requires:	%{name}-i18n >= %{EVRD}
Requires:	xlockmore
Recommends:	%{name}-themes
Recommends:	xterm
Recommends:	udisks-glue

%description
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

%package light
Summary:	A light version of Icewm
Group:		Graphical desktop/Icewm
Requires:	xdg-compliance
Recommends:	polkit-agent
# for update-menus
Requires(post):	desktop-common-data
Requires(postun):	desktop-common-data
Recommends:	%{name}-i18n
Conflicts:	desktop-common-data < 1:3.10-2

%description light
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is the light version with minimal features.

%package themes
Summary:	Extra themes of Icewm
Group:		Graphical desktop/Icewm
BuildArch: 	noarch
Conflicts:	%{name} < 1:1.3.7-2

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
Conflicts:	%{name} < 1:1.3.7-2

%description i18n
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is translation files for icewm window manager.

%prep
%setup -q -a 2 -a 9 -n %{name}-%{version}
%patch1 -p1 -b .xcin_bindy
%patch2 -p1 -b .defaultfont
%patch4 -p1 -b .winoptions
%patch10 -p1 -b .desktop
%patch12 -p1 -b .background
%patch25 -p1 -b .focus
%patch26 -p1 -b .mgapref
%patch28 -p1 -b .taskbar
%patch29 -p1 -b .litefix

rm -f po/en.* #- en is not a valid locale

chmod -R a+rX themes
find themes -type f | xargs chmod a-x

# build dirs
mkdir -p light default

%build
autoreconf -vfi

COMMON_CONFIGURE="--sysconfdir=%{_sysconfdir} --enable-i18n --enable-nls --with-libdir=%{_datadir}/%{name}"

echo "Light Version"
pushd light
	CONFIGURE_TOP=.. %configure $COMMON_CONFIGURE \
		--enable-lite \
		--enable-taskbar \
		--disable-winmenu \
		--disable-fribidi
	%make_build
popd

echo "Standard Version"
pushd default
	CONFIGURE_TOP=.. %configure $COMMON_CONFIGURE
	%make_build
        %make_build -C doc
popd

%install
%make_install -C default

for binary in %{light_apps}; do
   install light/src/${binary} %{buildroot}%{_bindir}/${binary}-light
done

rm -rf %{buildroot}%{_bindir}/icewm-set-gnomewm

for binary in %{default_apps}; do
    mv %{buildroot}%{_bindir}/${binary}  %{buildroot}%{_bindir}/${binary}-default
done

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

%find_lang %{name}

%postun light
if [ "$1" -eq 0 ]; then
    update-alternatives --remove icewm %{_bindir}/icewm-light
fi

%posttrans light
if [ "$1" -eq 1 ]; then
        if [ -e %{_datadir}/xsessions/07IceWM.desktop ]; then
                rm -rf %{_datadir}/xsessions/07IceWM.desktop
        fi
        if [ -e %{_sysconfdir}/X11/dm/Sessions/07IceWM.desktop ]; then
                rm -rf %{_sysconfdir}/X11/dm/Sessions/07IceWM.desktop
        fi

        update-alternatives \
                --install %{_bindir}/icewm icewm %{_bindir}/icewm-light 10 \
                --slave %{_bindir}/icewm-session icewm-session %{_bindir}/icewm-session-light \
                --slave %{_bindir}/icesh icesh %{_bindir}/icesh-light \
                --slave %{_bindir}/icewmbg icewmbg %{_bindir}/icewmbg-light \
                --slave %{_bindir}/icewmhint icewmhint %{_bindir}/icewmhint-light \
                --slave %{_bindir}/icewmtray icewmtray %{_bindir}/icewmtray-light
fi

%triggerun -- %{name} < 1:1.3.12-5
for app in icewm icesh icewmbg icewmhint icewm-session icewmtray icehelp; do
	if [ ! -L %{_bindir}/${app} ]; then
		rm -rf %{_bindir}/${app}
	fi
	update-alternatives --remove ${app} %{_bindir}/${app}
done

%triggerun -- %{name}-light < 1:1.3.12-13
for app in icesh icewmbg icewmhint icewm-session; do
	if [ -e %{_localstatedir}/lib/alternatives/${app} ]; then
		update-alternatives --remove ${app} %{_bindir}/${app}-light
	fi
done

%posttrans
if [ "$1" -eq 1 ]; then
	update-alternatives \
		--install %{_bindir}/icewm icewm %{_bindir}/icewm-default 20 \
		--slave %{_bindir}/icewm-session icewm-session %{_bindir}/icewm-session-default \
		--slave %{_bindir}/icesh icesh %{_bindir}/icesh-default \
		--slave %{_bindir}/icehelp icehelp %{_bindir}/icehelp-default \
		--slave %{_bindir}/icewmbg icewmbg %{_bindir}/icewmbg-default \
		--slave %{_bindir}/icewmhint icewmhint %{_bindir}/icewmhint-default \
		--slave %{_bindir}/icewmtray icewmtray %{_bindir}/icewmtray-default
fi

%postun
if [ "$1" -eq 0 ]; then
	update-alternatives --remove icewm %{_bindir}/icewm-default
fi

%files
%license COPYING
%doc README.md AUTHORS TODO THANKS NEWS
%doc doc/*.html doc/icewm.adoc
%ghost %{_bindir}/icewm
%ghost %{_bindir}/icewm-session
%ghost %{_bindir}/icesh
%ghost %{_bindir}/icewmbg
%ghost %{_bindir}/icewmhint
%ghost %{_bindir}/icewmtray
%ghost %{_bindir}/icehelp
%{_bindir}/icesh-default
%{_bindir}/icehelp-default
%{_bindir}/icewm-default
%{_bindir}/icewm-session-default
%{_bindir}/icewmbg-default
%{_bindir}/icewmhint-default
%{_bindir}/icewmtray-default
%{_mandir}/man1/%{name}.1.*

%files light
%license COPYING
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/icons
%dir %{_datadir}/%{name}/ledclock
%dir %{_datadir}/%{name}/taskbar
%dir %{_datadir}/%{name}/mailbox
%{_sysconfdir}/menu.d/%{name}
%{_datadir}/xsessions/%{name}.desktop
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
%ghost %{_bindir}/icewm
%ghost %{_bindir}/icewm-session
%ghost %{_bindir}/icesh
%ghost %{_bindir}/icewmbg
%ghost %{_bindir}/icewmhint
%ghost %{_bindir}/icewmtray
%{_bindir}/*-light

%files themes -f theme.list

%files i18n -f %{name}.lang
