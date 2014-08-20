from rucio.client.rseclient import RSEClient
rse = RSEClient()

#for x in rse.list_rses():
#    print x
#print rse.get_rse('TW-EOS00_AMS02DATADISK')

#print rse.get_rse_usage('TW-DPM01_TWGRIDSCRATCHDISK')
rse.set_rse_limits('TW-DPM01_AMS02DATADISK', 'MinFreeSpace', 300000000000)
rse.set_rse_usage('TW-DPM01_AMS02DATADISK', 'srm', 63150000000000, 63250000000000)
print rse.get_rse_usage('TW-DPM01_AMS02DATADISK')

