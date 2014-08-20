from rucio.client.fileclient import FileClient
file = FileClient()
scope = 'ams-2011B-ISS.B620-pass4'
lfn = '1368923945.00000001.root'
print file.list_file_replicas(scope, lfn)
