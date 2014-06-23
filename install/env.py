import subprocess
s = subprocess

#s.call("easy_install", "pip")
s.call("pip", "install", "dnspython")
s.call("easy_install", "virtualenv")
s.call("pip", "install", "virtualenvwrapper")
s.call("easy_install", "python-setuptools")
s.call("easy_install", "--upgrade")
s.call("curl" ,"-O" ,"http://python-distribute.org/distribute_setup.py")
s.call("sudo", "python", "distribute_setup.py")
s.call("sudo", "rm", "distribute_setup.py")

#export WORKON_HOME=$HOME/.virtualenvs
#export PROJECT_HOME=$HOME/Devel
#source /usr/bin/virtualenvwrapper.sh
#workon
#mkvirtualenv rucio
