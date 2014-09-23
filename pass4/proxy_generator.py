# -*- coding: utf-8 -*-

import subprocess, shlex, base64

cmd = 'voms-proxy-init --voms ams02.cern.ch --vomses /afs/cern.ch/user/c/cchao2/rucyio/etc/vomses/ams02.cern.ch-voms.grid.sinica.edu.tw --vomsdir /afs/cern.ch/user/c/cchao2/rucyio/etc/grid-security/vomsdir/'
cmd2 = 'kinit'
sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
with open('/afs/cern.ch/user/c/cchao2/.ssh/p', 'r') as file1:
    input = file1.read()

test = sub.communicate(input=base64.b64decode(input))
print test

sub2 = subprocess.Popen(shlex.split(cmd2), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
with open('/afs/cern.ch/user/c/cchao2/.ssh/p', 'r') as file2:
    input = file2.read()
test2 = sub2.communicate(input=base64.b64decode(input))
print test2
 
