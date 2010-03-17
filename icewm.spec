%define name	icewm
%define version	1.3.3
%define theirversion 1.3.1
%define release %mkrel 3

%define with_light 1
%define with_gnome 1
%{?_with_no_light: %{expand: %%global with_light 0}}
%{?_with_no_gnome: %{expand: %%global with_gnome 0}}

%define light_apps          icewm icesh icewmbg icewmhint icewm-session
%define default_apps        %{light_apps} icehelp
%define gnome_apps          %{default_apps} icesound

Name:		%{name}
Summary:	X11 Window Manager
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Graphical desktop/Icewm
Epoch:		1

URL:		http://www.icewm.org/
Source:		icewm-%{theirversion}.tar.bz2
Source1:	mandrake.xpm.bz2
Source2:	themes.tar.lzma
Source3:	icewm.menu
Source4:	icewm.menu-method
Source5:	icewm-16.png
Source6:	icewm-32.png
Source7:	icewm-48.png
Source8:	icewm-starticewm
Source9:	icewm-monochrome.tar.bz2
Source10:	icewm-galaxy.tar.bz2
Source12:	icewm-menu-xdg

Patch0:		icewm-1.3-dev-mdvconf.patch
# fix bindkey conflict xcin
Patch1:		icewm-1.2.26-xcin_bindy.patch
Patch2:		icewm-1.2.13pre3-defaultfont.patch
Patch3:		icewm-1.3-dev-always-fontset.patch
Patch4:		icewm-1.3-dev-winoptions.patch
Patch7:		icewm-1.2.0pre1-libsupc++.patch
Patch8:		icewm-1.2.5-lib64.patch
Patch10:	icewm-desktop.patch
Patch11:	icewmbg-1.2.14pre11-fixcrash.patch
Patch12:	icewm-1.2.14pre11-background.patch
Patch16:	icewm-1.3-dev-default-theme.patch
Patch18:	icewm-1.2.26-more_virtual_desktops.patch
Patch21:        icewm-1.3.1-fix-build.patch
Patch22:        icewm-1.3.0-gdkicon.patch
Patch23:	icewm-1.3.0-kdeicon.patch
Patch24:	icewm-1.3.0-fdoicon.patch
Patch25:	icewm-1.3.0-fix-focusing-on-raise.patch
# from Fedora
Patch100:	icewm-configure.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:  libx11-devel
BuildRequires:  libsm-devel
BuildRequires:  libxrandr-devel
BuildRequires:	autoconf2.5
BuildRequires:	gettext
BuildRequires:	libpcap-devel
BuildRequires:	xpm-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	gnomeui2-devel
BuildRequires:  libgdk_pixbuf2.0-devel
BuildRequires:  linuxdoc-tools
Requires:	mandrake_desk >= 7.1-1mdk, %{name}-light >= %epoch:%{version}
Requires:	xlockmore
# due to some theme move between icewm and icewm-light, urpmi needs help
Conflicts:	icewm-light < 1.2.20

%description
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

%package light
Summary:	A light version of Icewm
Group:		Graphical desktop/Icewm
Requires(post): menu >= 2.1.5-4mdk
Requires(postun): menu >= 2.1.5-4mdk
# due to some theme move between icewm and icewm-light, urpmi needs help
Conflicts:	icewm < 1.2.20

%description light
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is the light version with minimal features.


%if %{with_gnome}
%package gnome
Summary:        A gnome compatible version of Icewm
Group:          Graphical desktop/Icewm
Requires:       %{name}-light = %epoch:%{version}

%description gnome
Window Manager for X Window System. Can emulate the look of Windows'95, OS/2
Warp 3,4, Motif or the Java Metal GUI. Tries to take the best features of the
above systems. Features multiple workspaces, opaque move/resize, task bar,
window list, mailbox status, digital clock. Fast and small.

This is the GNOME version with full GNOME support and with some experimental 
options enabled.
%endif

%prep
%setup -q -a 2 -a 9 -a 10 -n %name-%theirversion
%patch0 -p1 -b .mdkconf
%patch1 -p1 -b .xcin_bindy
%patch2 -p1 -b .defaultfont
%patch3 -p1 -b .fontset
%patch4 -p1 -b .winoptions
%patch7 -p1 -b .libsupc++
%patch8 -p1 -b .lib64
%patch10 -p1 -b .desktop
%patch11 -p1 -b .nocrash
%patch12 -p1 -b .background
%patch16 -p1 -b .default-theme
%patch18 -p1 -b .more_desktop
%patch21 -p1
%patch22 -p1 -b .gdkicon
%patch23 -p1 -b .kdeicon
%patch24 -p1 -b .fdoicon
%patch25 -p1 -b .focus
%patch100 -p1 -b .configure
autoconf

rm -f po/en.* #- en is not a valid locale

bzcat %{SOURCE1} > lib/taskbar/mandrake.xpm
mv galaxy-icewm/Galaxy themes

chmod -R a+rX themes
find themes -type f | xargs chmod a-x

rm -r themes/Urbicande

%build

# moving everything to default
mv %{_builddir}/%{name}-%{theirversion} %{_builddir}/%{name}-%{theirversion}-default
install -d %{_builddir}/%{name}-%{theirversion}
mv %{_builddir}/%{name}-%{theirversion}-default %{_builddir}/%{name}-%{theirversion}/default
cd .
# then creating duplicates
for i in light gnome; do cp -a default $i; done

COMMON_CONFIGURE="--sysconfdir=/etc --enable-i18n --enable-nls --with-docdir=%{_docdir} --with-libdir=%{_datadir}/X11/%{name}"

%if %{with_light}
echo "Light Version"
(
	cd light
	CXXFLAGS="$RPM_OPT_FLAGS" %configure2_5x $COMMON_CONFIGURE --enable-lite
	%make
)
%endif

%if %{with_gnome}
echo "Gnome Version"
(
	cd gnome
	CXXFLAGS="$RPM_OPT_FLAGS" %configure2_5x $COMMON_CONFIGURE \
		--with-icesound=oss,esd --enable-menus-gnome2 \
		--enable-xfreetype --enable-antialiasing --enable-guievents
	%make
)
%endif

echo "Standard Version"
(
	cd default
	CXXFLAGS="$RPM_OPT_FLAGS" %configure2_5x $COMMON_CONFIGURE
	%make
        cd doc
        %make
)

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std -C default

# --with-bindir doesn't work
#install -d $RPM_BUILD_ROOT%{_bindir}
#mv $RPM_BUILD_ROOT/usr/bin/* $RPM_BUILD_ROOT%{_bindir}

%if %{with_light}
for binary in %{light_apps}; do 
   install light/src/${binary} $RPM_BUILD_ROOT%{_bindir}/${binary}-light
done
%endif

%if %{with_gnome}
for binary in %{gnome_apps}; do 
   install gnome/src/${binary} $RPM_BUILD_ROOT%{_bindir}/${binary}-gnome
done
%endif

cp -a default/themes $RPM_BUILD_ROOT%{_datadir}/X11/%{name}

%if %mdkversion < 200700
install -D -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_menudir}/%{name}
install -D -m755 %{SOURCE4} $RPM_BUILD_ROOT/etc/menu-methods/%{name}
%else
install -D -m755 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/menu.d/%{name}
%endif

# icon
install -D -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -D -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -D -m644 %{SOURCE7} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

excludes_patt="\(themes/Galaxy\|icewm/icons/\(app_\|xterm_\)\)"
(cd $RPM_BUILD_ROOT%{_datadir} ; find X11/%{name}/{icons,themes} ! -type d -printf "%{_datadir}/%%p\n") | grep -v "$excludes_patt" > other.list
(cd $RPM_BUILD_ROOT%{_datadir} ; find X11/%{name}/{icons,themes}   -type d -printf "%%%%dir %{_datadir}/%%p\n") | grep -v "$excludes_patt" >> other.list

# wmsession support
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmsession.d/
cat << EOF > $RPM_BUILD_ROOT/etc/X11/wmsession.d/07IceWM
NAME=IceWM
ICON=icewm-wmsession.xpm
EXEC=/usr/bin/starticewm
DESC=Lightweight desktop environment
SCRIPT:
exec /usr/bin/starticewm
EOF

install -m 755 %{SOURCE8} $RPM_BUILD_ROOT%{_bindir}/starticewm

# Dadou - 1.0.9-0.pre1.5mdk - Change default background color for MDK color
perl -pi -e "s!# DesktopBackgroundColor=.*!DesktopBackgroundColor=\"\"!" %buildroot%{_datadir}/X11/icewm/preferences

%find_lang %{name}
cat %{name}.lang >> other.list

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with_light}
%post light
for app in %{light_apps}; do
	update-alternatives --install %{_bindir}/${app} ${app} %{_bindir}/${app}-light 10
done
	
%{make_session}
if [ -x %{_bindir}/update-menus ]; then %{_bindir}/update-menus; fi

%postun light
if [ "$1" = 0 ]; then
    	if [ -x %{_bindir}/update-menus ]; then %{_bindir}/update-menus; fi
	for app in %{light_apps}; do
		update-alternatives --remove ${app} %{_bindir}/${app}-light
	done
fi
%{make_session}
%endif

%if %{with_gnome}
%post gnome
for app in %{light_apps}; do
	update-alternatives --install %{_bindir}/${app} ${app} %{_bindir}/${app}-gnome 30
done
%{make_session}

%postun gnome
if [ "$1" = 0 ]; then
	for app in %{light_apps}; do
		update-alternatives --remove ${app} %{_bindir}/${app}-gnome
	done
fi
%{make_session}
%endif

%post
for app in %{default_apps}; do
	update-alternatives --install %{_bindir}/${app} ${app} %{_bindir}/${app} 20
done
%{make_session}

%postun
if [ "$1" = 0 ]; then
	for app in %{default_apps}; do
		update-alternatives --remove ${app} %{_bindir}/${app}
	done
fi
%{make_session}

%files -f other.list
%defattr(-,root,root)
%doc default/README default/COPYING default/AUTHORS default/CHANGES default/TODO default/BUGS
%doc default/doc/*.html default/doc/icewm.sgml
%{_bindir}/icesh
%{_bindir}/icehelp
%{_bindir}/icewm
%{_bindir}/icewm-session
%{_bindir}/icewmbg
%{_bindir}/icewmhint
%{_bindir}/icewmtray

%files light
%defattr(-,root,root)
%doc light/COPYING
%dir %{_datadir}/X11/%{name}
%dir %{_datadir}/X11/%{name}/themes
%dir %{_datadir}/X11/%{name}/icons
%dir %{_datadir}/X11/%{name}/ledclock
%dir %{_datadir}/X11/%{name}/taskbar
%dir %{_datadir}/X11/%{name}/mailbox
%if %mdkversion < 200700
/etc/menu-methods/%{name}
%else
/etc/menu.d/%{name}
%endif
%config(noreplace) /etc/X11/wmsession.d/*
%{_bindir}/starticewm
%{_datadir}/X11/%{name}/mailbox/*
%{_datadir}/X11/%{name}/taskbar/*
%{_datadir}/X11/%{name}/ledclock/*
%{_datadir}/X11/%{name}/icons/app_*
%{_datadir}/X11/%{name}/icons/xterm_*
%{_datadir}/X11/%{name}/keys
%{_datadir}/X11/%{name}/menu
%{_datadir}/X11/%{name}/preferences
%{_datadir}/X11/%{name}/toolbar
%{_datadir}/X11/%{name}/winoptions
#%{_datadir}/X11/%{name}/programs
%{_datadir}/X11/%{name}/themes/Galaxy
%if %mdkversion < 200700
%{_menudir}/%{name}
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%if %{with_light}
%{_bindir}/*-light
%endif

%if %{with_gnome}
%files gnome
%defattr(-,root,root)
%doc gnome/COPYING
%{_bindir}/*-gnome
%endif


