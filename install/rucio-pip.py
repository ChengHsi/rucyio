#I don't know why rucio won't install these modules automatically, but here it is

import subprocess

with open("/opt/rucio/tools/pip-requires") as f:
    for line in f:
        line = line.rstrip('\n')
        line = line.split()
        #print line[0].rstrip()
        if line and "#" not in line[0]:
            print line[0]
            subprocess.call(["pip", "install", line[0]])

pip_list=["argcomplete==0.8.0", 'dogpile.cache==0.5.3', 'kerberos==1.1.1', 'requests-kerberos==0.4.0', 'wsgiref==0.1.2', 'urllib3==1.7.1', 'requests==2.2.1', 'distribute==0.7.3', "kerberos==1.1.1", "requests-kerberos==0.4.0", "MySQL-python"]
easy_list = ["PIL==1.1.7"]

for i in pip_list:
    subprocess.call(["pip", "install", i])

for i in easy_list:
    subprocess.call(["easy_install", i])

subprocess.call(["wget", "http://pysftp.googlecode.com/files/pysftp-0.2.2.tar.gz"])
subprocess.call(["pip", "install", "pysftp-0.2.2.tar.gz"])
subprocess.call(["rm", "-rf", "pysftp-0.2.2.tar.gz"])



