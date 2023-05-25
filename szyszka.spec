%bcond_without check
%global __cargo_skip_build 0

%global uuid com.github.qarmin.szyszka
%global pkgname szyszka

# Do not upgrade without testing!
# Looks like compiling with system provided rust packages is not posible at this time. 
# Online installation is not possible too due strange errors:
# "error: no matching package named `audiotags` found
# location searched: registry `https://github.com/rust-lang/crates.io-index`"
# For some reason this crates can't be found. So as workaround, we can create own vendor pack.
# Download szyszka .tar.gz source, unpack it, cd and install 'dnf install cargo-vendor'
# Then inside szyszka dir (or any other cargo/rust project) run in terminal command: 'cargo vendor'
# This create new dir called vendor and download here all needed crates dependencies.
# When process finish, compress it as vendor.tar.xz and upload to file-store. Place here as Source1.

Summary:	Szyszka is fast and powerful file renamer
Name:		szyszka
Version:	3.0.0
Release:	1
License:	MIT
URL:		https://github.com/qarmin/szyszka
Source0:	https://github.com/qarmin/szyszka/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	vendor.tar.xz

BuildRequires:	rust-packaging
BuildRequires:	rust
BuildRequires:	rust-src
BuildRequires:	cargo
BuildRequires:	cargo-c
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(atk)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	hicolor-icon-theme

%global srcroot %{_sourcedir}/%{pkgname}-%{version}

%description
Szyszka is a simple but powerful and fast bulk file renamer.
Features:
Written in Rust
Available for Linux, Mac and Windows
Simple GUI created using GTK3
Multiple rules which can be freely combined:
Replace text
Trim text
Add text
Add numbers
Purge text
Change letters to upper/lowercase
Custom rules
Ability to edit, reorder rules and results
Handle even hundreds thousands of records

%prep
%autosetup -p1
tar -xf %{SOURCE1} -C %{_builddir}
%define cargo_registry %{_builddir}/vendor

%cargo_prep

%build
#cargo_build

cargo build --release

%install
# Cargo install is broken. For some reason it not intall any files.
#cargo_install
mkdir -p %{buildroot}%{_bindir}/
install -Dm755 ./target/release/szyszka -t %{buildroot}%{_bindir}
install -Dm644 ./data/icons/com.github.qarmin.szyszka.svg -t %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
install -Dm644 ./data/com.github.qarmin.szyszka.desktop -t %{buildroot}%{_datadir}/applications/
install -Dm644 ./data/com.github.qarmin.szyszka.metainfo.xml -t %{buildroot}%{_datadir}/metainfo

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE
%{_bindir}/%{pkgname}
%{_datadir}/applications/com.github.qarmin.szyszka.desktop
%{_iconsdir}/hicolor/scalable/apps/com.github.qarmin.szyszka.svg
%{_datadir}/metainfo/com.github.qarmin.szyszka.metainfo.xml
