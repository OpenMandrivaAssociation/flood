%define snap r500244

Summary:	A benchmarking tool for Apache2
Name:		flood
Version:	1.1
Release:	%mkrel 0.%{snap}.3
License:	Apache License
Group:		System/Servers
URL:		http://httpd.apache.org/test/flood/
Source0:	flood-1.1-%{snap}.tar.bz2
Patch0:		flood-openssl-version.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	apr-devel >= 1.2.2
BuildRequires:	apr-util-devel >= 1.2.2
BuildRequires:	apache-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	libxslt-proc
Requires:	openssl

%description
Flood is a profile-driven HTTP load tester. It can be used to
gather important performance metrics for your website.

%prep

%setup -q -n flood
%patch0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
		
for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%build
#########################################################################################
# configure and build phase
#

export WANT_AUTOCONF_2_5=1
#libtoolize --copy --force; aclocal-1.7; autoconf; automake-1.7 --add-missing
autoconf

%serverbuild

export CFLAGS="%{optflags}"

# We need to re-run ./buildconf because of any applied patch(es)
#./buildconf

%configure2_5x \
    --cache-file=config.cache \
    --with-apr=%{_bindir}/apr-1-config \
    --with-apr-util=%{_bindir}/apu-1-config \
    --with-openssl=%{_includedir} \
    --enable-ssl \
    --with-capath=%{_sysconfdir}/pki/flood

%make 

# make docs
mkdir -p manual
xsltproc -o manual/ %{_datadir}/sgml/docbook/xsl-stylesheets/xhtml/chunk.xsl docs/docbook/flood.xml

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
#########################################################################################
# install phase
#

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/pki/flood/private

# install flood
install -m0755 flood %{buildroot}%{_sbindir}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

%files
%defattr(644,root,root,755)
%doc CHANGES CONFIG DESIGN LICENSE NOTICE STATUS examples manual
%dir %{_sysconfdir}/pki/flood
%dir %{_sysconfdir}/pki/flood/private
%attr(0755,root,root) %{_sbindir}/flood


