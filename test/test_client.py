from rucio.client.client import Client
import sys
import pdb; pdb.set_trace()
client = Client()
# scope = sys.argv[1]
# name = sys.argv[2]
# rep.list_replicas([{'scope':'ams-2011B-ISS.B620-pass4', 'name':'1340252898.00981893.root'}])
# for x in rep.list_replicas([{'scope':scope, 'name':name}]):
#     print x

# print client.list_scopes()
for x in client.scope_list('ams-user-chenghsi'):
    print x
