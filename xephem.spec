#
# TODO: Check INDI interface (anyone with telescope?), probably change
#	fifo dir (/usr/share/xephem/fifo) as it needs to be writeable.
#	And how it cooperates with http://indi.sf.net?
#
Summary:	Interactive astronomy program
Summary(pl.UTF-8):	Interaktywny program astronomiczny
Name:		xephem
Version:	3.7.7
Release:	2
License:	distributable with free-unices distros, free for non-profit non-commercial purposes
Group:		X11/Applications/Science
Source0:	http://www.clearskyinstitute.com/xephem/%{name}-%{version}.tgz
# Source0-md5:	27c67061a89085bf2b0d4e9deb758a79
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}_sites
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-format.patch
Patch2:		%{name}-3.7.7_openssl.patch
Patch3:		%{name}-3.7.7_openssl_earthmenu.patch
URL:		http://www.clearskyinstitute.com/xephem/
BuildRequires:	groff
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	motif-devel
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
%patch2 -p3
%patch3 -p3
%patch0 -p1
%patch1 -p1

sed -i "s#X11R6/lib#X11R6/%{_lib}#g" GUI/xephem/Makefile
sed -i "s#/usr/local#%{_datadir}#g" GUI/xephem/tools/xephemdbd/start-xephemdbd.pl

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

%{__make} -C tools/simpleINDI \
	CC="%{__cc}" \
	CFLAGS="-ffast-math %{rpmcflags} -I../../../../liblilxml -I../../../../libastro -I../../../../libip"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_appdefsdir}}

cp -p GUI/xephem/xephem $RPM_BUILD_ROOT%{_bindir}
cp -a GUI/xephem/auxil $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/catalogs $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fifos $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fits $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/gallery $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/help $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/lo $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -p GUI/xephem/xephem.man $RPM_BUILD_ROOT%{_mandir}/man1/xephem.1

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
echo XEphem.ShareDir: %{_datadir}/%{name} > $RPM_BUILD_ROOT%{_appdefsdir}/XEphem

# INDI drivers
cp -p GUI/xephem/tools/simpleINDI/simpleINDI $RPM_BUILD_ROOT%{_bindir}
cp -p GUI/xephem/tools/lx200xed/lx200xed $RPM_BUILD_ROOT%{_bindir}
cp -p GUI/xephem/tools/xedb/xedb $RPM_BUILD_ROOT%{_bindir}
cp -p GUI/xephem/tools/xephemdbd/xephemdbd $RPM_BUILD_ROOT%{_bindir}
# xephemdbd.html and xephemdbd.pl are used for WWW interface to xephemdbd
# one can make http server subpackage
cp -p GUI/xephem/tools/xephemdbd/start-xephemdbd.pl $RPM_BUILD_ROOT%{_bindir}
cp -p GUI/xephem/auxil/*.pl $RPM_BUILD_ROOT%{_bindir}

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
%doc GUI/xephem/tools/lx200xed/README-lx200xed
%doc GUI/xephem/tools/xedb/README-xedb GUI/xephem/tools/xephemdbd/README-xephemdbd

%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/xephem
%{_mandir}/man1/*
%exclude %{_mandir}/man1/xephem.1*
