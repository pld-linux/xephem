Summary:	Interactive astronomy program
Summary(pl):	Interaktywny program astronomiczny
Name:		xephem
Version:	3.5.2
Release:	6
License:	distributable with free-unices distros, free for non-profit non-commercial purposes
Group:		X11/Applications/Science
Source0:	http://www.clearskyinstitute.com/cgi-bin/download/%{name}-%{version}.tar.gz
# Source0-md5:	5820b51667531743d0db0e7f712a9fae
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	http://www.clearskyinstitute.com/cgi-bin/download/xephem-3.5.2.pdf
# Source3-md5:	2bcff3adf673d7b1e95512bbada47abf
URL:		http://www.clearskyinstitute.com/xephem/
BuildRequires:	XFree86-devel
BuildRequires:	openmotif-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XEphem  \eks-i-'fem\   n.   [X Window + Ephemeris]   (1990)
XEphem is a star-charting, sky-simulating, ephemeris-generating
celestial virtuoso.

%description -l pl
XEphem  \eks-i-'fem\   n.   [X Window + Ephemeris]   (1990)
XEphem jest programem sporz±dzaj±cym mapê gwiazd, symuluj±cym niebo,
efemerydalnie generuj±cym sferê niebiesk± wirtuozem. Udostêpnia wiele
informacji o satelitach Ziemi, Uk³adzie S³onecznym i odleg³ych
obiektach astronomicznych, w formie graficznej i liczbowej, w uk³adzie
geocentrycznym, heliocentrycznym i topocentrycznym.

%package tools
Summary:	Additional tools for use with XEphem
Summary(pl):	Dodatkowe narzêdzia dla XEphema
Group:		X11/Applications/Science
Requires:	%{name} = %{version}

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
Requires:	%{name} = %{version}

%description doc
XEphem documentation in PDF format.

%description doc -l pl
Dokumentacja XEphema w formacie PDF.

%prep
%setup -q

mv GUI/xephem/tools/lx200xed/README GUI/xephem/tools/lx200xed/README-lx

%build
%{__make} -C libastro	CC="%{__cc}" CFLAGS="%{rpmcflags}"
%{__make} -C libip	CC="%{__cc}" CFLAGS="%{rpmcflags} -I../libastro"
cd GUI/xephem
xmkmf -a
%{__make} CC="%{__cc}" CDEBUGFLAGS="%{rpmcflags}"
cd tools/lx200xed
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -I../../../../libastro"
cd ../xephemdbd
%{__make} CC="%{__cc}" CFLAGS="%{rpmcflags} -I../../../../libastro"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_applnkdir}/Scientific/Astronomy,%{_pixmapsdir}} \
	$RPM_BUILD_ROOT{%{_libdir}/X11/app-defaults,%{_docdir}/%{name}-%{version}}

install GUI/xephem/xephem $RPM_BUILD_ROOT%{_bindir}
cp -a GUI/xephem/auxil $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/catalogs $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fifos $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a GUI/xephem/fits $RPM_BUILD_ROOT%{_datadir}/%{name}

install GUI/xephem/xephem.man $RPM_BUILD_ROOT%{_mandir}/man1/xephem.1

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Scientific/Astronomy
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
echo XEphem.ShareDir: %{_datadir}/%{name} > $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults/XEphem

install GUI/xephem/tools/lx200xed/lx200xed $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/tools/xephemdbd/xephemdbd $RPM_BUILD_ROOT%{_bindir}
install GUI/xephem/tools/xephemdbd/*.pl $RPM_BUILD_ROOT%{_bindir}

install GUI/xephem/tools/*.pl $RPM_BUILD_ROOT%{_bindir}
cp -f Copyright LICENSE

install %{SOURCE3} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_bindir}/xephem
%{_datadir}/%{name}
%{_applnkdir}/Scientific/Astronomy/*
%{_pixmapsdir}/*
%{_libdir}/X11/app-defaults/*
%{_mandir}/man1/*

%files tools
%defattr(644,root,root,755)
%doc GUI/xephem/tools/lx200xed/README-lx GUI/xephem/tools/xephemdbd/{INSTALL,README}
%doc GUI/xephem/tools/xephemdbd/*.html
%attr(755,root,root) %{_bindir}/lx200xed
%attr(755,root,root) %{_bindir}/xephemdbd
%attr(755,root,root) %{_bindir}/*.pl

%files doc
%{_docdir}/%{name}-%{version}
