# This Script Sets all Quotas for User Account to their respective USER_RSEID as set in the DICOS-WEB
# Also Max Quota is set for all RSE for the root Account, and Max Quota is set for all SCRATCHDISK for special account panda

for i in `rucio list-rses`; do rucio-admin account set-limits root $i 9223372036854775807;done
for i in `rucio list-scopes|grep bioinfo-user`; do rucio-admin account set-limits ${i:13} TW-EOS03_BIOINFOSCRATCHDISK 10000000000000;done
for i in `rucio list-scopes|grep ams-user`; do rucio-admin account set-limits ${i:9} TW-EOS01_NONDET_AMS02SCRATCHDISK 10000000000000;done
for i in `rucio list-scopes|grep ams-user`; do rucio-admin account set-limits ${i:9} TW-EOS02_AMS02DATADISK 10000000000000;done
for i in `rucio list-scopes|grep twgrid-user`; do rucio-admin account set-limits ${i:12} PHYS-EOS01_TWGRIDSCRATCHDISK 10000000000000;done
for i in `rucio list-rses|grep SCRATCHDISK`; do rucio-admin account set-limits panda $i 9223372036854775807;done

