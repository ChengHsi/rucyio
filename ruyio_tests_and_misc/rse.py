from rucio.client.rseclient import RSEClient
rse = RSEClient()

for x in rse.list_rses():
    print x
#print rse.get_rse('TW-EOS00_AMS02DATADISK')


