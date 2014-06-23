from rucio.client.rseclient import RSEClient
rse = RSEClient()

print rse.list_rse_attributes('TW-EOS00_AMS02DATADISK')


