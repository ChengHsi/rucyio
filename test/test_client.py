from rucio.client.client import Client
import sys
import pdb; pdb.set_trace()
client = Client()
# scope = sys.argv[1]
# name = sys.argv[2]
# scope = 'ams-2011B-ISS.B620-pass4'
# name = 'file20150708T164717'
scope = 'ams-user-chenghsi'
# name = sys.argv[1]
name = 'Old_dataset'
new_name = 'NewNew_dataset'
# client.list_replicas([{'scope':'ams-2011B-ISS.B620-pass4', 'name':'1340252898.00981893.root'}])
# for x in client.list_replicas([{'scope':scope, 'name':name}]):
#     print x

# client.set_metadata(scope=scope, name=name, key='lifetime', value=0)

# print client.list_scopes()
# for x in client.scope_list('ams-user-chenghsi'):
#     print x


def test_rename(scope, name, new_name, type):
    client.rename_did(scope, name, new_name, type)

test_rename(scope, name, new_name, 'dataset')
