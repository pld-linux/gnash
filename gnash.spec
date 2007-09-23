#
# Conditional build:
%bcond_without	kde	# don't build klash plugin for Konqueror
%bcond_with	tests
#
Summary:	Gnash - free Flash movie player
Summary(pl.UTF-8):	Gnash - wolnodostępny odtwarzacz filmów Flash
Name:		gnash
Version:	0.8.1
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.gnu.org/gnu/gnash/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	5f80a25cb7a37fb351d28fd2097d8f3e
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	agg-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	boost-bind-devel
BuildRequires:	boost-date_time-devel
BuildRequires:	boost-devel
BuildRequires:	boost-thread-devel
BuildRequires:	cairo-devel
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	expat-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	glib2-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gtk+2-devel >= 1:2.0
BuildRequires:	gtkglext-devel
%{?with_kde:BuildRequires:	kdelibs-devel >= 3.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig
BuildRequires:	scrollkeeper
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	zlib-devel
BuildRequires:	zlib-devel
%if %{with tests}
BuildRequires:	ming-devel
BuildRequires:	mtasc
BuildRequires:	swfmill
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnash is originally based on the code of GameSWF, by Thatcher Ulrich.
GameSWF is the most advanced of the free Flash movie player projects,
and implements a fairly broad set of Flash Format v7 compliance.
GameSWF was unsupported public domain software though, and not really
setup to be an industrial strength project that could be used by
everyone that uses Firefox. So in early December of 2005, GameSWF was
forked, and the code rearranged in GNU project style.

%description -l pl.UTF-8
Gnash jest oryginalnie oparty na kodzie GameSWF autorstwa Thatchera
Ulricha. GameSWF to najbardziej zaawansowany z wolnodostępnych
odtwarzaczy filmów Flash i implementuje w miarę szeroki podzbiór
formatu Flash v7. GameSWF był jednak nie wspieranym oprogramowaniem
public domain, więc na początku grudnia 2005 GameSWF został
odgałęziony, a kod przeorganizowany w stylu projektu GNU.

%package -n konqueror-plugin-klash
Summary:	Klash plugin for Konqueror
Summary(pl.UTF-8):	Wtyczka Klash dla Konquerora
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	konqueror

%description -n konqueror-plugin-klash
Klash plugin for Konqueror for displaying Flash using Gnash library.

%description -n konqueror-plugin-klash -l pl.UTF-8
Wtyczka Klash dla Konquerora służąca do wyświetlania Flasha przy
użyciu biblioteki Gnash.

%package -n browser-plugin-%{name}
Summary:	Browser plugin for Flash rendering
Summary(pl.UTF-8):	Wtyczka przeglądarki wyświetlająca animacje Flash
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Provides:	browser(flash)
Obsoletes:	browser-plugin-gplflash2
Obsoletes:	mozilla-plugin-gplflash2

%description -n browser-plugin-%{name}
Browser plugin for rendering of Flash animations based on gnash
library.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka przeglądarki wyświetlająca animacje Flash oparta na bibliotece
gnash.

%prep
%setup -q

# contains libtool.m4 copy
rm -f macros/libltdl.m4

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
# use gstreamer as media handler - ffmpeg doesn't have extern "C" wrappers
%configure \
	--disable-static \
	--enable-ghelp \
	%{?with_kde:--enable-klash} \
	--enable-media=gst \
	--enable-pthreads \
	--enable-visibility \
	--with-plugindir=%{_browserpluginsdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# useless without --enable-sdk-install, which does nothing atm
rm -f $RPM_BUILD_ROOT%{_libdir}/libgnash*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gnash
%attr(755,root,root) %{_bindir}/gparser
%attr(755,root,root) %{_bindir}/gprocessor
%attr(755,root,root) %{_bindir}/gtk-gnash
%{_datadir}/gnash
%{_mandir}/man1/gnash.1*
%dir %{_libdir}/gnash
%attr(755,root,root) %{_libdir}/gnash/libgnashamf*.so
%attr(755,root,root) %{_libdir}/gnash/libgnashbackend*.so
%attr(755,root,root) %{_libdir}/gnash/libgnashbase*.so
%attr(755,root,root) %{_libdir}/gnash/libgnashgeo*.so
%attr(755,root,root) %{_libdir}/gnash/libgnashserver*.so

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/libgnashplugin.so

%if %{with kde}
%files -n konqueror-plugin-klash
%defattr(644,root,root,755)
%doc plugin/klash/README
%attr(755,root,root) %{_bindir}/kde-gnash
%{_libdir}/kde3/libklashpart.la
%attr(755,root,root) %{_libdir}/kde3/libklashpart.so
%{_datadir}/apps/klash
%{_datadir}/services/klash_part.desktop
%endif
