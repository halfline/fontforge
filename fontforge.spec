Name:           fontforge
Version:        0.0
Release:        1.20040824
Epoch:          0
Summary:        An outline and bitmap font editor

Group:          Applications/Publishing
License:        BSD
URL:            http://fontforge.sourceforge.net/
Source0:        http://fontforge.sourceforge.net/fontforge_full-20040824.tgz
Source1:        fontforge.desktop
Source2:        http://fontforge.sourceforge.net/fontforge_htdocs-20040824.tgz
Source3:        pfaicon.gif
Patch1:         fontforge-20040618-docview.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       htmlview
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  libungif-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  XFree86-devel
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
BuildRequires:  libuninameslist-devel
Obsoletes:      pfaedit

%description 
FontForge (former PfaEdit) is a font editor for outline and bitmap
fonts. It supports a range of font formats, including PostScript
(ASCII and binary Type 1, some Type 3 and Type 0), TrueType, OpenType
(Type2) and CID-keyed fonts.

%prep
%setup -q -n fontforge-20040824
%patch1 -p2 -b .docview

mkdir htdocs
tar xzf %{SOURCE2} -C htdocs
rm -rf htdocs/scripts
mkdir cidmaps
tar xzf htdocs/cidmaps.tgz -C cidmaps

find . -name "CVS" -type d -print | xargs rm -r 


%build
%configure --with-regular-link --with-freetype-bytecode=no
# Parallell make not working.
make DOCDIR=%{_docdir}/%{name}-%{version}/htdocs

%install
rm -rf $RPM_BUILD_ROOT
# make install DESTDIR=$RPM_BUILD_ROOT fails.
%makeinstall
install -p -m 644 cidmaps/Adobe* $RPM_BUILD_ROOT%{_datadir}/fontforge
rm -f $RPM_BUILD_ROOT%{_libdir}/libgunicode.la $RPM_BUILD_ROOT%{_libdir}/libgdraw.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libgunicode.so $RPM_BUILD_ROOT%{_libdir}/libgdraw.so

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
convert %{SOURCE3} fontforge.png
install -m 644 fontforge.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/

desktop-file-install \
  --vendor fedora                                          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications            \
  --add-category X-Fedora                                  \
  %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS INSTALL LICENSE README htdocs
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/*.1*


%changelog
* Sun Sep 19 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040824
- Updated to 20040824.

* Wed Jun 30 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040618
- Updated to 20040618.

* Wed Jun  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040601
- Updated to 20040601.

* Tue May 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040509
- Updated to 20040509.

* Thu Apr 15 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040410
- Updated to 20040410.

* Sun Mar 28 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20040321
- Updated to 20040321.
- Changed package name from pfaedit to fontforge.
- Added Obsoletes: pfaedit.

* Mon Mar 15 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.8.040310
- Updated to 040310.

* Sat Feb  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.8.040204
- Updated to 040204.
- Removed some unnecessary directory ownerships (bug 1061).

* Sun Jan 25 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.8.040111
- Updated documentation to 040111.

* Sun Jan 11 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.040111
- Updated to 040111.
- Converted spec file to UTF-8.

* Wed Jan  7 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.040102
- Updated to 040102.

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031210
- Updated to 031210.

* Sat Dec 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031205
- Updated to 031205.

* Fri Nov 28 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.7.031123
- Updated to 031123.

* Wed Nov 12 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.6.031110
- Updated to 031110.
- Eliminated build patch; incorporated in upstream tarball.
- Re-added documentation tarball since no longer included in source tarball.
- Added pfaicon.gif as Packaging directory disappeared from tarball.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.5.031012
- Refetched sources since upstream suddenly decided to change them (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.4.031012
- Build req libuninameslist-devel instead of libuninameslist.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.3.031012
- Fixed non-standard value in desktop file (bug 497).
- Added libuninameslist support.
- Removed separate documentation tarball; mostly identical to those in source (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.2.031012
- Patched to use dynamic linking instead of dlopen'ing (bug 497).
- Patched to use htmlview and use installed documentation (bug 497).
- Added build req libxml2-devel (bug 497).
- Disabled parallell make (bug 497).
- Added desktop entry (bug 497).

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.031012
- Updated to 031012.
- Removed .so links.
- Removed empty AUTHORS file.
- Removed the samples subpackage. 

* Mon Sep 22 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030904
- Updated to 030904.

* Wed Sep  3 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030831
- Updated to 030831.

* Tue Aug 12 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030803
- Updated to 030803.

* Mon Jul 21 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.3.030702
- Added font samples.
- Added ldconfig to post and postun.
- Added samples subpackage.

* Sun Jul  6 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.2.030702
- Removed README-MS and README-MacOSX from documentation.

* Thu Jul  3 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.0-0.fdr.1.030512
- Initial RPM release based on Mandrake's PfaEdit-030512 RPM.
