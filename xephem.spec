Summary:	An interactive astronomical ephemeris program for X Window
Summary(pl):	Interaktywny program astronomiczny dla X Window
Name:		xephem
Version:	3.2.3
Release:	7
Copyright:	Freely redistributable/modifiable if attributed, no warranty
Group:		X11/Applications
Group(pl):	X11/Aplikacje
Source0:	ftp://iraf.noao.edu/contrib/xephem/%{name}-%{version}.tar.gz
Patch0:		xephem-3.2.3-config.patch

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description

%description -l pl
XEphem jest interaktywnym programem astronomicznym dla X Window
wykorzystuj±cym bibliotekê Motif. Udostêpnia wiele informacji o
satelitach Ziemi, Uk³adzie S³onecznym i odleg³ych obiektach
astronomicznych, w formie graficznej i liczbowej, w uk³adzie
geocentrycznym, heliocentrycznym i topocentrycznym.

%prep
%setup -q
%patch -p1

%build
cd libastro
xmkmf
%{__make}

cd ../GUI/xephem
xmkmf
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
XS=GUI/xephem
XL=$RPM_BUILD_ROOT%{_libdir}/xephem

install -d $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk

echo "XEphem name \"XEphem\" " > $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem description \"An Interactive Astronomy Ephemeris\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem exec \"xephem &\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem group \"Applications\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem

install -s $XS/xephem $RPM_BUILD_ROOT%{_bindir}/xephem

install $XS/xephem.man $RPM_BUILD_ROOT%{_mandir}/man1/xephem.1x

install -d $XL/auxil
install -d $XL/catalogs
install -d $XL/catalogs/gsc
install -d $XL/fifos
install -d $XL/tools
install -d $XL/tools/gsc
install -d $XL/tools/xephemdbd

install $XS/auxil/*		$XL/auxil
install $XS/catalogs/*		$XL/catalogs
install $XS/fifos/*		$XL/fifos
install $XS/tools/[Raejtm]*	$XL/tools
install $XS/tools/gsc/*	$XL/tools/gsc
install $XS/tools/xephemdbd/*	$XL/tools/xephemdbd

install $XS/XEphem.ad \
	$RPM_BUILD_ROOT%{_prefix}/X11R6/lib/X11/app-defaults/XEphem

cat > README.linux <<'EOT'
This XEphem binary RPM is compiled to link statically to
Lesstif 0.89.9. The source RPM will build dynamically 
linked to your installed version of LessTif.   -C. Kulesa
EOT

%files
%defattr(644,root,root,755)
%doc Copyright
%doc HISTORY
%doc INSTALL
%doc README

%doc README.linux

%doc GUI/xephem/XEphem.ad

%{_prefix}/X11R6/bin/xephem
%{_mandir}/man1/xephem.1x
%{_libdir}/xephem
%{_prefix}/X11R6/lib/X11/app-defaults/XEphem
%{_prefix}/X11R6/share/applnk/XEphem
