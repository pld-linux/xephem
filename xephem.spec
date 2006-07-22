Summary:	Interactive astronomy program
Summary(pl):	Interaktywny program astronomiczny
Name:		xephem
Version:	3.7.1
Release:	1
License:	distributable with free-unices distros, free for non-profit non-commercial purposes
Group:		X11/Applications/Science
Source0:	http://www.clearskyinstitute.com/xephem/%{name}-%{version}.tar.gz
# Source0-md5:	a7a89469f1c0681d186344ef96941b8d
Source1:	%{name}.desktop
Source2:	%{name}.png
# http://www.clearskyinstitute.com/xephem/help/xephem.html
Source3:	http://distfiles.pld-linux.org/src/xephem-reference-manual-html-3.7.1.tar.bz2
# Source3-md5:	b5951f5cc23a9cbc91697df395987f09
Source4:	%{name}_sites
Patch0:		%{name}-makefile.patch
URL:		http://www.clearskyinstitute.com/xephem/
BuildRequires:	XFree86-devel
BuildRequires:	openmotif-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdefsdir	/usr/X11R6/lib/X11/app-defaults

%description
XEphem \eks-i-'fem\ n. [X Window + Ephemeris] (1990)
XEphem is a star-charting, sky-simulating, ephemeris-generating
celestial virtuoso.

%description -l pl
XEphem \eks-i-'fem\ n. [X Window + Ephemeris] (1990)
XEphem jest programem sporz±dzaj±cym mapê gwiazd, symuluj±cym niebo,
efemerydalnie generuj±cym sferê niebiesk± wirtuozem. Udostêpnia wiele
informacji o satelitach Ziemi, Uk³adzie S³onecznym i odleg³ych
obiektach astronomicznych, w formie graficznej i liczbowej, w uk³adzie
geocentrycznym, heliocentrycznym i topocentrycznym.

%package tools
Summary:	Additional tools for use with XEphem
Summary(pl):	Dodatkowe narzêdzia dla XEphema
Group:		X11/Applications/Science
Requires:	%{name} = %{version}-%{release}

%description tools
astorb2edb - convert astorb.txt to 2 .edb files,
mpcorb2edb - convert MPCORB.DAT to 2 .edb files,
lx200xed - a daemon to connect XEphem to a Meade LX200 telescope,
XEphemdbd - is a filter to find astronomical objects within a given
	    field of view.

%description tools -l pl
astorb2edb - konwertuje astorb.txt do 2 plików .edb,
mpcorb2edb - konwertuje MPCORB.DAT do 2 plików .edb,
lx200xed - demon do po³±czenia XEphema z teleskopem Meade LX200,
XEphemdbd - filt do odnajdywania obiektów astronomicznych wg zadanych
	    pól opisu.

%package doc
Summary:	XEphem documentation in PDF
Summary(pl):	Dokumentacja XEphema w PDF-ie
Group:		X11/Applications/Science
Requires:	%{name} = %{version}-%{release}

%description doc
XEphem reference manual in HTML format.

%description doc -l pl
Podrêcznik XEphema w formacie HTML.

%prep
%setup -q
%patch0 -p1

sed -i "s#X11R6/lib#X11R6/%{_lib}#g" GUI/xephem/Makefile

mv GUI/xephem/tools/lx200xed/README GUI/xephem/tools/lx200xed/README-lx
mv GUI/xephem/tools/indi/README GUI/xephem/tools/indi/README-indi
mv GUI/xephem/tools/xedb/README GUI/xephem/tools/xedb/README-xedb
mv GUI/xephem/tools/xephemdbd/README GUI/xephem/tools/xephemdbd/README-xephemdbd

%build

cd GUI/xephem

%{__make} \
	CC="%{__cc}" \
	CDEBUGFLAGS="%{rpmcflags}"

%{__make} -C tools/lx200xed \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I../../../../libastro"

%{__make} -C tools/xephemdbd \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I../../../../GUI/xephem -I../../../../libastro -I../../../../libip"

%{__make} -C tools/xedb \
        CC="%{__cc}" \
        CFLAGS="%{rpmcflags} -I../../../../libastro"

%{__make} drivers -C tools/indi \
        CC="%{__cc}" \
        CFLAGS="%{rpmcflags} -I../../../../liblilxml -I../../../../libastro -I../../../../libip"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/doc,%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_appdefsdir}}

rm -f GUI/xephem/auxil/xephem_sites
cp %{SOURCE4} GUI/xephem/auxil/

install GUI/xephem/xephem $RPM_BUILD_ROOT%{_bindir}
cp -a GUI/xephem/auxil $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/catalogs $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fifos $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fits $RPM_BUILD_ROOT%{_datadir}/%{name}

install GUI/xephem/xephem.man $RPM_BUILD_ROOT%{_mandir}/man1/xephem.1

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
echo XEphem.ShareDir: %{_datadir}/%{name} > $RPM_BUILD_ROOT%{_appdefsdir}/XEphem

install GUI/xephem/tools/lx200xed/lx200xed $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/tools/xephemdbd/xephemdbd $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/xephemdbd/*.pl $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/auxil/*.pl $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/xephemdbd/*.pl $RPM_BUILD_ROOT%{_bindir}
cp -f Copyright LICENSE

install %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/xephem
%{_datadir}/%{name}
%{_desktopdir}/*
%{_pixmapsdir}/*
%{_appdefsdir}/*
%{_mandir}/man1/*

%files tools
%defattr(644,root,root,755)
%doc GUI/xephem/tools/lx200xed/README-lx GUI/xephem/tools/xephemdbd/README-xephemdbd
%doc GUI/xephem/tools/indi/README-indi GUI/xephem/tools/indi/README-indi

%doc GUI/xephem/tools/xephemdbd/*.html
%attr(755,root,root) %{_bindir}/lx200xed
%attr(755,root,root) %{_bindir}/xephemdbd
%attr(755,root,root) %{_bindir}/*.pl

%files doc
%defattr(644,root,root,755)
%{_datadir}/%{name}/doc
