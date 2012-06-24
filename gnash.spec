#
# Conditional build:
%bcond_without	kde	# don't build klash plugin for Konqueror
#
Summary:	Gnash - free Flash movie player
Summary(pl):	Gnash - wolnodost�pny odtwarzacz film�w Flash
Name:		gnash
Version:	0.7.2
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.gnu.org/gnu/gnash/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	ccef0f45be01a4c2992b46c2363a514f
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	boost-devel
BuildRequires:	cairo-devel
%{?with_kde:BuildRequires:	kdelibs-devel >= 3.0}
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	gtkglext-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	scrollkeeper
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	zlib-devel
Requires:	browser-plugins(%{_target_base_arch})
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnash is originally based on the code of GameSWF, by Thatcher Ulrich.
GameSWF is the most advanced of the free Flash movie player projects,
and implements a fairly broad set of Flash Format v7 compliance.
GameSWF was unsupported public domain software though, and not really
setup to be an industrial strength project that could be used by
everyone that uses Firefox. So in early December of 2005, GameSWF was
forked, and the code rearranged in GNU project style.

%description -l pl
Gnash jest oryginalnie oparty na kodzie GameSWF autorstwa Thatchera
Ulricha. GameSWF to najbardziej zaawansowany z wolnodost�pnych
odtwarzaczy film�w Flash i implementuje w miar� szeroki podzbi�r
formatu Flash v7. GameSWF by� jednak nie wspieranym oprogramowaniem
public domain, wi�c na pocz�tku grudnia 2005 GameSWF zosta�
odga��ziony, a kod przeorganizowany w stylu projektu GNU.

%package -n konqueror-plugin-klash
Summary:	Klash plugin for Konqueror
Summary(pl):	Wtyczka Klash dla Konquerora
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	konqueror

%description -n konqueror-plugin-klash
Klash plugin for Konqueror for displaying Flash using Gnash library.

%description -n konqueror-plugin-klash -l pl
Wtyczka Klash dla Konquerora s�u��ca do wy�wietlania Flasha przy
u�yciu biblioteki Gnash.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
# mmm?? %{_lib} or drop?
export PATH=/usr/lib/mozilla-firefox:$PATH
%configure \
	--disable-static \
	--enable-ghelp \
	%{?with_kde:--enable-klash} \
	--enable-mp3 \
	--enable-pthreads \
	--with-plugindir=%{_libdir}/browser-plugins
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# useless without --enable-sdk-install
rm -f $RPM_BUILD_ROOT%{_libdir}/libgnash*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gnash
%attr(755,root,root) %{_bindir}/gparser
%attr(755,root,root) %{_bindir}/gprocessor
%dir %{_datadir}/gnash
%{_datadir}/gnash/gnash_128_96.ico
%{_mandir}/man1/gnash.1*
# removed in install section
#%attr(755,root,root) %{_libdir}/libgnash*.so.*.*.*
%attr(755,root,root) %{_libdir}/browser-plugins/libgnashplugin.so

%if %{with kde}
%files -n konqueror-plugin-klash
%defattr(644,root,root,755)
%doc plugin/klash/README
%attr(755,root,root) %{_bindir}/klash
%{_libdir}/kde3/libklashpart.la
%attr(755,root,root) %{_libdir}/kde3/libklashpart.so
%{_datadir}/apps/klash
%{_datadir}/config/klashrc
%{_datadir}/services/klash_part.desktop
%endif
