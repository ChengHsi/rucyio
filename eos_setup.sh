# source /afs/cern.ch/project/eos/installation/ams/etc/setup.sh
# unset LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64/
kinit
voms-proxy-init --voms ams02.cern.ch --vomses /afs/cern.ch/user/c/cchao2/rucyio/etc/vomses/ams02.cern.ch-voms.grid.sinica.edu.tw --vomsdir /afs/cern.ch/user/c/cchao2/rucyio/etc/grid-security/vomsdir/

