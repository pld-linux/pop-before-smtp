%include	/usr/lib/rpm/macros.perl
Summary:	watch log for pop/imap auth, notify Postfix to allow relay
Summary(pl):	Przesy³anie poczty przez postfiksa na podstawie logowañ przez POP/IMAP
Name:		pop-before-smtp
Version:	1.28
Release:	1
License:	Freely Redistributable
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://people.oven.com/bet/pop-before-smtp/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-config.patch
Requires:	postfix
BuildRequires:	perl-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch0 -p1 -b .wiget

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig,rc.d/init.d},%{_sbindir},%{_mandir}/man8}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/popbsmtp
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/popbsmtp
install pop-before-smtp $RPM_BUILD_ROOT%{_sbindir}/

pod2man pop-before-smtp >$RPM_BUILD_ROOT%{_mandir}/man8/pop-before-smtp.8
echo ".so pop-before-smtp" >$RPM_BUILD_ROOT%{_mandir}/man8/popbsmtp.8

gzip -9nf README

%post
/sbin/chkconfig popbsmtp reset
if [ -f /var/lock/subsys/popbsmtp ]; then
	%{_sysconfdir}/rc.d/init.d/popbsmtp restart >&2 
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_sbindir}/pop-before-smtp
%attr(755,root,root) /etc/rc.d/init.d/popbsmtp
%config(noreplace) %verify(not mtime size md5) /etc/sysconfig/popbsmtp
%{_mandir}/man8/*
