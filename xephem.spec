Summary:	An interactive astronomical ephemeris program for X Window
Summary(pl):	Interaktywny program astronomiczny dla X Window
Name:		xephem
Version:	3.2.3
Release:	7
Copyright:	Freely redistributable/modifiable if attributed, no warranty
Group:		Applications/Scientific
######		/home/users/ig0r/rpm/groups: no such file
Group(pl):	Aplikacje/Naukowe
Source0:	ftp://iraf.noao.edu/contrib/xephem/%{name}-%{version}.tar.gz
Patch0:		xephem-3.2.3-config.patch
%description
%description -l pl
XEphem jest interaktywnym programem astronomicznym dla X Window
wykorzystuj±cym bibliotekê Motif. Udostêpnia wiele informacji o satelitach
Ziemi, Uk³adzie S³onecznym i odleg³ych obiektach astronomicznych, w formie
graficznej i liczbowej, w uk³adzie geocentrycznym, heliocentrycznym i
topocentrycznym.

%prep
%setup -q
%patch -p1

%build
cd libastro
xmkmf
make

cd ../GUI/xephem
xmkmf
make

%install
XS=GUI/xephem
XL=$RPM_BUILD_ROOT%{_libdir}/xephem

install -d $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk

echo "XEphem name \"XEphem\" " > $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem description \"An Interactive Astronomy Ephemeris\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem exec \"xephem &\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem
echo "XEphem group \"Applications\" " >> $RPM_BUILD_ROOT%{_prefix}/X11R6/share/applnk/XEphem

install -s -m 755 -o 0 -g 0 $XS/xephem $RPM_BUILD_ROOT%{_bindir}/xephem

install -o 0 -g 0 $XS/xephem.man $RPM_BUILD_ROOT%{_prefix}/man/man1/xephem.1x

install -d -m 755 -o 0 -g 0 $XL/auxil
install -d -m 755 -o 0 -g 0 $XL/catalogs
install -d -m 755 -o 0 -g 0 $XL/catalogs/gsc
install -d -m 755 -o 0 -g 0 $XL/fifos
install -d -m 755 -o 0 -g 0 $XL/tools
install -d -m 755 -o 0 -g 0 $XL/tools/gsc
install -d -m 755 -o 0 -g 0 $XL/tools/xephemdbd

install -o 0 -g 0 $XS/auxil/*		$XL/auxil
install -o 0 -g 0 $XS/catalogs/*		$XL/catalogs
install -o 0 -g 0 $XS/fifos/*		$XL/fifos
install -o 0 -g 0 $XS/tools/[Raejtm]*	$XL/tools
install -o 0 -g 0 $XS/tools/gsc/*	$XL/tools/gsc
install -o 0 -g 0 $XS/tools/xephemdbd/*	$XL/tools/xephemdbd

install -o 0 -g 0 $XS/XEphem.ad \
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
