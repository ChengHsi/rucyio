from rucio.client.client import Client
import sys
import pdb; pdb.set_trace()
client = Client()
# scope = sys.argv[1]
# name = sys.argv[2]
# scope = 'ams-2011B-ISS.B620-pass4'
# name = '1340252898.00981893.root'
scope = 'ams-user-chenghsi'
name = 'file20150721T110241'
# client.list_replicas([{'scope':'ams-2011B-ISS.B620-pass4', 'name':'1340252898.00981893.root'}])
for x in client.list_replicas([{'scope':scope, 'name':name}]):
    print x

# print client.list_scopes()
# for x in client.scope_list('ams-user-chenghsi'):
#     print x