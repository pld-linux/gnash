Summary:	Gnash - free Flash movie player
Summary(pl):	Gnash - wolnodostêpny odtwarzacz filmów Flash
Name:		gnash
Version:	0.7.1
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	ftp://ftp.gnu.org/gnu/gnash/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	d860981aeaac0fc941a28abc3c24223c
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gtkglext-devel
BuildRequires:	gtk+2-devel >= 2.0
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
Ulricha. GameSWF to najbardziej zaawansowany z wolnodostêpnych
odtwarzaczy filmów Flash i implementuje w miarê szeroki podzbiór
formatu Flash v7. GameSWF by³ jednak nie wspieranym oprogramowaniem
public domain, wiêc na pocz±tku grudnia 2005 GameSWF zosta³
odga³êziony, a kod przeorganizowany w stylu projektu GNU.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
export PATH=/usr/lib/mozilla-firefox/:$PATH
%configure \
	--disable-static \
	--enable-ghelp \
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
%attr(755,root,root) %{_libdir}/libgnash*.so.*.*.*
%attr(755,root,root) %{_libdir}/browser-plugins/libgnashplugin.so
