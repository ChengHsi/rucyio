easy_install pip
pip install dnspython
easy_install virtualenv
pip install virtualenvwrapper
easy_install python-setuptools
#easy_install --upgrade
#curl -O http://python-distribute.org/distribute_setup.py
#sudo python distribute_setup.py
#sudo rm distribute_setup.py
yum install -y git
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/bin/virtualenvwrapper.sh
#workon
mkvirtualenv rucio
