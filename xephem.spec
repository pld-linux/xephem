#
# TODO: Check INDI interface (anyone with telescope?), probably change
#	fifo dir (/usr/share/xephem/fifo) as it needs to be writeable.
#	And how it cooperates with http://indi.sf.net?
#	Consider using system-wide libjpeg instead of shipped libjpegd
#
Summary:	Interactive astronomy program
Summary(pl.UTF-8):	Interaktywny program astronomiczny
Name:		xephem
Version:	3.7.4
Release:	1
License:	distributable with free-unices distros, free for non-profit non-commercial purposes
Group:		X11/Applications/Science
Source0:	http://97.74.56.125/free/%{name}-%{version}.tar.gz
# Source0-md5:	4e9290609f36df469a2ba5a1b4fffd46
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}_sites
Patch0:		%{name}-makefile.patch
URL:		http://www.clearskyinstitute.com/xephem/
BuildRequires:	groff
BuildRequires:	libpng-devel
BuildRequires:	openmotif-devel
BuildRequires:	sed >= 4.0
Requires:	xorg-lib-libXt >= 1.0.0
Obsoletes:	xephem-doc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/share/X11/app-defaults

%description
XEphem \eks-i-'fem\ n. [X Window + Ephemeris] (1990)
XEphem is a star-charting, sky-simulating, ephemeris-generating
celestial virtuoso.

%description -l pl.UTF-8
XEphem \eks-i-'fem\ n. [X Window + Ephemeris] (1990)
XEphem jest programem sporządzającym mapę gwiazd, symulującym niebo,
efemerydalnie generującym sferę niebieską wirtuozem. Udostępnia wiele
informacji o satelitach Ziemi, Układzie Słonecznym i odległych
obiektach astronomicznych, w formie graficznej i liczbowej, w układzie
geocentrycznym, heliocentrycznym i topocentrycznym.

%package tools
Summary:	Additional tools for use with XEphem
Summary(pl.UTF-8):	Dodatkowe narzędzia dla XEphema
Group:		X11/Applications/Science
Requires:	%{name} = %{version}-%{release}

%description tools
astorb2edb - convert astorb.txt to 2 .edb files,
mpcorb2edb - convert MPCORB.DAT to 2 .edb files,
INDI - tools for connecting telescope using INDI interface,
lx200xed - a daemon to connect XEphem to a Meade LX200 telescope,
xedb - tool to generate ephemeris data from .edb files,
XEphemdbd - filter to find astronomical objects within a given
	    field of view.

%description tools -l pl.UTF-8
astorb2edb - konwertuje astorb.txt do 2 plików .edb,
mpcorb2edb - konwertuje MPCORB.DAT do 2 plików .edb,
INDI - narzędzia do podłączenia teleskopu za pomocą interfejsu INDI,
lx200xed - demon do połączenia XEphema z teleskopem Meade LX200,
xedb - narzędzie do generowania danych efemerycznych z plików .edb,
XEphemdbd - filtr do odnajdywania obiektów astronomicznych wg zadanych
	    pól opisu.

%prep
%setup -q
%patch0 -p1

sed -i "s#X11R6/lib#X11R6/%{_lib}#g" GUI/xephem/Makefile
sed -i "s#/usr/local#%{_datadir}#g" GUI/xephem/tools/xephemdbd/start-xephemdbd.pl

mv GUI/xephem/tools/indi/README GUI/xephem/tools/indi/README-indi
mv GUI/xephem/tools/lx200xed/README GUI/xephem/tools/lx200xed/README-lx200xed
mv GUI/xephem/tools/xedb/README GUI/xephem/tools/xedb/README-xedb
mv GUI/xephem/tools/xephemdbd/README GUI/xephem/tools/xephemdbd/README-xephemdbd
mv -f Copyright LICENSE

cat %{SOURCE3} >> GUI/xephem/auxil/xephem_sites

%build

# build these libraries first in order to have CFLAGS passed
%{__make} -C libastro \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{__make} -C libip \
	CC="%{__cc}" \
	CFLAGS="-I../libastro %{rpmcflags}"

%{__make} -C libjpegd \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{__make} -C liblilxml \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

cd GUI/xephem

%{__make} \
	CC="%{__cc}" \
	CLDFLAGS="%{rpmcflags}"

%{__make} -C tools/lx200xed \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I../../../../libastro"

%{__make} -C tools/xephemdbd \
	CC="%{__cc}" \
	CFLAGS="-ffast-math %{rpmcflags} -I../../../../GUI/xephem -I../../../../libastro -I../../../../libip"

%{__make} -C tools/xedb \
	CC="%{__cc}" \
	CFLAGS="-ffast-math %{rpmcflags} -I../../../../libastro"

%{__make} -C tools/indi \
	CC="%{__cc}" \
	CFLAGS="-ffast-math %{rpmcflags} -I../../../../liblilxml -I../../../../libastro -I../../../../libip"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_appdefsdir}}

install GUI/xephem/xephem $RPM_BUILD_ROOT%{_bindir}
cp -a GUI/xephem/auxil $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/catalogs $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fifos $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fits $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/gallery $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/help $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/lo $RPM_BUILD_ROOT%{_datadir}/%{name}

install GUI/xephem/xephem.man $RPM_BUILD_ROOT%{_mandir}/man1/xephem.1

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
echo XEphem.ShareDir: %{_datadir}/%{name} > $RPM_BUILD_ROOT%{_appdefsdir}/XEphem

# INDI drivers
install GUI/xephem/tools/indi/cam $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/ota $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/security $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/tmount $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/wx $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/tools/indi/evalINDI $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/getINDI $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/indiserver $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/indi/setINDI $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/lx200xed/lx200xed $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/xedb/xedb $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/xephemdbd/xephemdbd $RPM_BUILD_ROOT%{_bindir}
# xephemdbd.html and xephemdbd.pl are used for WWW interface to xephemdbd
# one can make http server subpackage
install GUI/xephem/tools/xephemdbd/start-xephemdbd.pl $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/auxil/*.pl $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/tools/indi/evalINDI.man $RPM_BUILD_ROOT%{_mandir}/man1/evalINDI.1
install GUI/xephem/tools/indi/getINDI.man $RPM_BUILD_ROOT%{_mandir}/man1/getINDI.1
install GUI/xephem/tools/indi/indidevapi.man $RPM_BUILD_ROOT%{_mandir}/man1/indidevapi.1
install GUI/xephem/tools/indi/indiserver.man $RPM_BUILD_ROOT%{_mandir}/man1/indiserver.1
install GUI/xephem/tools/indi/setINDI.man $RPM_BUILD_ROOT%{_mandir}/man1/setINDI.1

install GUI/xephem/tools/indi/*.fts $RPM_BUILD_ROOT%{_datadir}/%{name}/fits

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/xephem
%{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_appdefsdir}/*
%{_mandir}/man1/xephem.1*

%files tools
%defattr(644,root,root,755)
%doc GUI/xephem/tools/indi/README-indi GUI/xephem/tools/lx200xed/README-lx200xed
%doc GUI/xephem/tools/xedb/README-xedb GUI/xephem/tools/xephemdbd/README-xephemdbd

%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/xephem
%{_mandir}/man1/*
%exclude %{_mandir}/man1/xephem.1*
