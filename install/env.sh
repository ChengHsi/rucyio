easy_install pip
pip install dnspython
easy_install virtualenv
pip install virtualenvwrapper
easy_install python-setuptools
#easy_install --upgrade
curl -O http://python-distribute.org/distribute_setup.py
sudo python distribute_setup.py
sudo rm distribute_setup.py
yum install -y git
yum install -y gcc.x86_64
#yum install krb5-config
yum install -y krb5-devel.x86_64
yum install -y krb5-workstation.x86_64
yum install -y python-devel
yum install -y mysql-server-5.1.73-3.el6_5.x86_64
yum install -y mysql-libs-5.1.73-3.el6_5.x86_64
yum install -y mysql-5.1.73-3.el6_5.x86_64
yum install -y mysql-devel-5.1.73-3.el6_5.x86_64
service mysqld start
mysqladmin -u root password asgcddm
#mysqladmin -uroot -p asgcddm create rucio
#export WORKON_HOME=$HOME/.virtualenvs
#export PROJECT_HOME=$HOME/Devel
#source /usr/bin/virtualenvwrapper.sh
#workon
#mkvirtualenv rucio
