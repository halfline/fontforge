%define docs_version 20080302
%define gettext_package FontForge

Name:           fontforge
Version:        20080309
Release:        1%{?dist}
Summary:        Outline and bitmap font editor

Group:          Applications/Publishing
License:        BSD
URL:            http://fontforge.sourceforge.net/
Source0:        http://downloads.sourceforge.net/fontforge/fontforge_full-%{version}.tar.bz2
Source1:        fontforge.desktop
Source2:        http://downloads.sourceforge.net/fontforge/fontforge_htdocs-%{docs_version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       xdg-utils

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  libungif-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libuninameslist-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  gettext

Obsoletes:      pfaedit
Provides:       pfaedit

%description
FontForge (former PfaEdit) is a font editor for outline and bitmap
fonts. It supports a range of font formats, including PostScript
(ASCII and binary Type 1, some Type 3 and Type 0), TrueType, OpenType
(Type2) and CID-keyed fonts.

%package devel
Summary: Development tools for fontforge
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package includes the libraries and header files you will need
to compile applications against fontforge.

%prep
%setup -q -n %{name}-%{version}

mkdir htdocs
tar xjf %{SOURCE2} -C htdocs
rm -rf htdocs/scripts
chmod 644 htdocs/*.gif
chmod 644 htdocs/*.html
chmod 644 htdocs/*.png
rm -rf htdocs/flags/CVS
mkdir cidmaps
tar xzf htdocs/cidmaps.tgz -C cidmaps

# Fix bad line terminators
%{__sed} -i 's/\r//' htdocs/Big5.txt
%{__sed} -i 's/\r//' htdocs/corpchar.txt

%build
%configure --with-freetype-bytecode=no

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -p -m 644 cidmaps/Adobe* $RPM_BUILD_ROOT%{_datadir}/fontforge
rm -f $RPM_BUILD_ROOT%{_libdir}/libg{draw,unicode}.{la,so}

install -Dpm 644 htdocs/ffanvil32.png \
  $RPM_BUILD_ROOT%{_datadir}/pixmaps/fontforge.png

desktop-file-install \
  --vendor fedora                                          \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications            \
  --add-category X-Fedora                                  \
  %{SOURCE1}

# The fontforge makefiles install htdocs as well, but we
# prefer to have them under the standard RPM location, so
# remove the extra copy
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/fontforge

# remove unneeded .la and .a files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# Find translations
%find_lang %{gettext_package}

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{gettext_package}.lang
%defattr(-,root,root,-)
%doc AUTHORS LICENSE htdocs
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_datadir}/applications/*fontforge.desktop
%{_datadir}/fontforge
%{_datadir}/pixmaps/fontforge.png
%{_mandir}/man1/*.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/fontforge/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Mar 17 2008 Kevin Fenzi <kevin@tummy.com> - 20080309-1
- Upgrade to 20080309
- Fixes bug 437833

* Mon Mar 03 2008 Kevin Fenzi <kevin@tummy.com> - 20080302-2
- Commit new sources

* Mon Mar 03 2008 Kevin Fenzi <kevin@tummy.com> - 20080302-1
- Update to upstream 20080302

* Sun Mar 02 2008 Kevin Fenzi <kevin@tummy.com> - 20080203-2
- Change Requires from htmlview to xdg-utils (bz 312691)

* Sat Mar 01 2008 Kevin Fenzi <kevin@tummy.com> - 20080203-1
- Update to upstream 20080203
- Add new devel subpackage

* Sun Dec 02 2007 Roozbeh Pournader <roozbeh@farsiweb.info> - 20071110-1
- Update to upstream 20071110

* Sun Oct 21 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
☢ 20071002-1
⚠ quick & dirty version bump to start working on F9 font packages

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 20070511-2
- Rebuild for BuildID 

* Thu Jun  7 2007 Kevin Fenzi <kevin@tummy.com> - 20070511-1
- Update to upstream 20070511
- Remove some leftover CVS bits
- Remove useless .pc file.

* Fri Dec 22 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061220-1
- Update to upstream 20061220

* Sat Dec 09 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061025-2
- Add patch to fix fsSelection problem with DejaVu ExtraLight

* Sat Nov 25 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20061025-1
- Update to 20061025
- Patch to correct usFirstCharIndex (George Williams)

* Fri Oct 20 2006 Kevin Fenzi <kevin@tummy.com> - 20061019-1
- Update to 20061019

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 20060822-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Kevin Fenzi <kevin@tummy.com> - 20060822-1
- Update to 20060822
- Remove unneeded patch
- Add flag to compile right with giflib

* Sun Jun 18 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-7
- Add BuildRequires on gettext, to make sure the package builds in minimal
  mock environments

* Mon Feb 13 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-6
- Rebuild for Fedora Extras 5

* Sun Feb 12 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-5
- Add patch to fix crash (#181052, George Williams)

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-4
- Add "BuildRequires:" on libXt-devel and xorg-x11-proto-devel

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-3
- Really remove XFree86-devel BuildReq

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-2
- Remove XFree86-devel BuildReq

* Wed Feb 01 2006 Roozbeh Pournader <roozbeh@farsiweb.info> - 20060125-1
- Update to 20060125 (bug #170177)
- Update docs to 20060114
- Change versioning to reflect upstream and follow packaging guidelines
- Provide pfaedit (bug #176548)
- Use %%{?dist} tag (bug #176472)
- Add localizations
- No need to remove CVS subdir: fixed upstream
- No need to covert man pages to UTF-8: fixed upstream
- Fixed DOS line terminators
- Use parallel build

* Sat Jul 30 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050729.fc4
- Update to 20050729
- Remove .docview patch, looking for HTMLview is upstream so no longer needed

* Tue May 10 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050502.fc4
- Update to 20050502
- Fix the build to look for the docs where we install them

* Sat Mar 19 2005 Owen Taylor <otaylor@redhat.com> - 0.0-2.20050310
- Update to 20050310

* Sat Jan 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.0-2.20041231
- Avoid RPATH.
- Convert man pages to UTF-8.
- Fix pkgconfig and doc file permissions.
- Use updated upstream icon.
- Don't include installation documentation.

* Mon Jan 17 2005 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-1.20041231
- Updated to 20041231.

* Thu Oct 28 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.20041014
- Updated to 20041014.

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
