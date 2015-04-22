from ubuntu:14.04.2
maintainer guido.stevens@cosent.net
run apt-get update && apt-get install -y python-dev gcc make zlib1g-dev libjpeg-dev python-virtualenv git-core libfreetype6-dev gettext python-pip libxslt1-dev python-lxml sudo jed
run apt-get update && apt-get install -y gfortran libgfortran3 libatlas-dev libatlas3gf-base python-numpy python-scipy
run update-alternatives --set libblas.so.3 /usr/lib/atlas-base/atlas/libblas.so.3
run update-alternatives --set liblapack.so.3 /usr/lib/atlas-base/atlas/liblapack.so.3

run locale-gen nl_NL.UTF-8 nl_NL

run useradd -m -d /app app && echo "app:app" | chpasswd && adduser app sudo
run ln -s /usr/include/freetype2/ /usr/include/freetype
run echo plone.app.learning > /etc/debian_chroot
cmd ["/bin/bash"]
