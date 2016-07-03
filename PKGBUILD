# Maintainer: Your Name Max Chesterfield <chestm007@hotmail.com
pkgname=pyAlsi
pkgver=0.1
pkgrel=1
pkgdesc="python rewrite of alsi, with a few more features"
arch=()
url=""
license=('GPL')
groups=()
depends=('python2', 'pip2')
makedepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
changelog=
source=($pkgname-$pkgver.tar.gz)
noextract=()
md5sums=() #autofill using updpkgsums

build() {
  cd "$pkgname-$pkgver"

  ./configure --prefix=/usr
  make
}

package() {
  cd "$srcdir/$pkgname-$pkgver"

  python setup.py install --root="$pkgdir/" --optimize=1
}