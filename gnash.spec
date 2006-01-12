Summary:	Gnash - free Flash movie player
Summary(pl):	Gnash - wolnodostêpny odtwarzacz filmów Flash
Name:		gnash
Version:	0.7
%define	snap	20051226
Release:	0.%{snap}.1
License:	GPL v2+
Group:		X11/Applications/Multimedia
Source0:	http://www.gnu.org/software/gnash/releases/%{name}-%{snap}.tar.bz2
# Source0-md5:	16d3261d0ec22be7cc738e30b42dc9ac
Patch0:		%{name}-build.patch
URL:		http://www.gnu.org/software/gnash/
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	XFree86-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel
BuildRequires:	scrollkeeper
BuildRequires:	zlib-devel
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-plugin \
	--disable-static \
	--enable-pthreads
# doesn't build with mozilla 1.7.x
#	--with-firefox-includes=/usr/include/mozilla/plugin \
#	--with-firefox-libraries=%{_libdir}
%{__make}
#	FIREFOX_CFLAGS="-I/usr/include/mozilla/plugin -I/usr/include/mozilla/java -I/usr/include/nspr" \
#	FIREFOX_PLUGINS=%{_libdir}/mozilla

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
#	FIREFOX_PLUGINS=%{_libdir}/mozilla

# unusable
rm -f $RPM_BUILD_ROOT%{_includedir}/*.h
rm -f $RPM_BUILD_ROOT%{_libdir}/gnash/*.{la,so}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnash
%attr(755,root,root) %{_bindir}/gparser
%attr(755,root,root) %{_bindir}/gprocessor
%dir %{_libdir}/gnash
%attr(755,root,root) %{_libdir}/gnash/lib*.so.*
%{_datadir}/gnash
%{_omf_dest_dir}/gnash
