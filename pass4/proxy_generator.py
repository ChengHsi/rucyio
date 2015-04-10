# -*- coding: utf-8 -*-

import subprocess
import shlex
import base64

# cmd = 'voms-proxy-init --voms ams02.cern.ch --vomses /afs/cern.ch/user/c/cchao2/rucyio/etc/vomses/ams02.cern.ch-voms.grid.sinica.edu.tw --vomsdir /afs/cern.ch/user/c/cchao2/rucyio/etc/grid-security/vomsdir/'
cmd = 'voms-proxy-init --voms ams02.cern.ch:/ams02.cern.ch/Role=pilot --vomses /afs/cern.ch/user/c/cchao2/rucyio/etc/vomses/ams02.cern.ch-voms.grid.sinica.edu.tw --vomsdir /afs/cern.ch/user/c/cchao2/rucyio/etc/grid-security/vomsdir --valid 596522:59 --vomslife 596522:59'
# cmd2 = 'kinit'
sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
with open('/afs/cern.ch/user/c/cchao2/.ssh/p', 'r') as file1:
    input = file1.read()

test = sub.communicate(input=base64.b64decode(input))
print test
cmd2 = '/usr/sue/kinit -R; /usr/bin/aklog'
sub2 = subprocess.Popen(shlex.split(cmd2), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
print sub2.communicate()
# with open('/afs/cern.ch/user/c/cchao2/.ssh/p', 'r') as file2:
#     input = file2.read()
# test2 = sub2.communicate(input=base64.b64decode(input))
#   print test2
# cmd3 = 'source /afs/cern.ch/project/eos/installation/ams/etc/setup.sh; unset LD_LIBRARY_PATH;export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64/:$LD_LIBRARY_PATH'
# sub3 = subprocess.Popen(shlex.split(cmd2), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
# print sub3.communicate()
