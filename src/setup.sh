#!/bin/bash
debian_pkgs=("libfontconfig" "wget" "python3")
python_pkgs=("selenium" "click" "wget")

# install debian packages
for pkg in "${debian_pkgs[@]}"
do
  echo $(dpkg-query -W -f='${Status}\n' $pkg)
  if [[ ! $(dpkg-query -W -f='${Status}\n' $pkg) == "install ok installed" ]]; then
    echo "$pkg not found. Installing"
    sudo apt-get install $pkg
  else
    echo "Skipping $pkg...it is already installed."
  fi
done

# install python packages
for pkg in "${python_pkgs[@]}"
do
  pip install $pkg
done

# download custom code
if [ ! -d $HOME/3rd-party/phantomjs-2.1.1-linux-x86_64 ]; then
  wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && tar -xvf $HOME/3rd-party/phantomjs-2.1.1-linux-x86_64
  tar xvf $HOME/3rd-party/phantomjs-2.1.1-linux-x86_64.tar.bz2 $HOME/3rd-party/phantomjs-2.1.1-linux-x86_64
fi
 

