%include	/usr/lib/rpm/macros.perl
Summary:	Watch log for pop/imap auth, notify Postfix to allow relay
Summary(pl):	Przesy³anie poczty przez postfiksa na podstawie logowañ przez POP/IMAP
Name:		pop-before-smtp
Version:	1.29
Release:	5
License:	freely distributable
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/popbsmtp/%{name}-%{version}.tar.gz
# Source0-md5:	012d7e9b4f73572eb499562ba252701d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-config.patch
Patch1:		%{name}-comments.patch
Patch2:		%{name}-db_location.patch
Patch3:		%{name}-ignore_ipv6.patch
Patch4:		%{name}-OK.patch
Patch5:		%{name}-mappedv6.patch
URL:		http://popbsmtp.sourceforge.net/
BuildRequires:	perl-devel
BuildRequires:	perl-File-Tail
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	postfix
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      /var/lib/popbsmtp

%description
Spam prevention requires preventing open relaying through email
servers. However, legit users want to be able to relay. If legit users
always stayed in one spot, they'd be easy to describe to the daemon.
However, what with roving laptops, logins from home, etc., legit users
refuse to stay in one spot. pop-before-smtp watches the mail log,
looking for successful pop/imap logins, and posts the originating IP
address into a database which can be checked by Postfix, to allow
relaying for people who have recently downloaded their email.

%description -l pl
Pop-before-smtp obserwuje log systemu pocztowego, szukaj±c udanych
zalogowañ przez protokó³ POP lub IMAP. Adres z którego nast±pi³o udane
logowanie jest dopisywany do bazy danych, na podstawie której postfix
mo¿e zezwalaæ na wysy³anie przez niego poczty.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2	-p1
%patch3	-p0
%patch4	-p1
%patch5	-p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig,rc.d/init.d},%{_sbindir},%{_mandir}/man8,%{_pkglibdir}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/popbsmtp
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/popbsmtp
install pop-before-smtp $RPM_BUILD_ROOT%{_sbindir}/

pod2man pop-before-smtp >$RPM_BUILD_ROOT%{_mandir}/man8/pop-before-smtp.8
echo ".so pop-before-smtp.8" >$RPM_BUILD_ROOT%{_mandir}/man8/popbsmtp.8

touch $RPM_BUILD_ROOT%{_pkglibdir}/pop-before-smtp.db

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add popbsmtp
if [ -f /var/lock/subsys/popbsmtp ]; then
	/etc/rc.d/init.d/popbsmtp restart >&2
else
	echo "Run \"/etc/rc.d/init.d/popbsmtp start\" to start pop-before-smtp daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/popbsmtp ]; then
		/etc/rc.d/init.d/popbsmtp stop
	fi
	/sbin/chkconfig --del popbsmtp
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/pop-before-smtp
%attr(754,root,root) /etc/rc.d/init.d/popbsmtp
%config(noreplace) %verify(not mtime size md5) /etc/sysconfig/popbsmtp
%{_mandir}/man8/*
%dir %{_pkglibdir}
%ghost %{_pkglibdir}/pop-before-smtp.db
