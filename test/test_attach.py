import sys
from rucio.client import Client as RucioClient
client = RucioClient()
# scope = sys.argv[1]
# name = sys.argv[2]
# rep.list_replicas([{'scope':'ams-2011B-ISS.B620-pass4', 'name':'1340252898.00981893.root'}])
# for x in rep.list_replicas([{'scope':scope, 'name':name}]):
#     print x
from rucio.common.utils import generate_uuid
account = 'chenghsi'
scope = 'twgrid-user-chenghsi'
name = 'file20150709T105442'
client.attach_dids(scope, 'New_Dataset', [{'scope': scope, 'name': '0.txt',
                  'bytes': 29, 'adler32': '6e190697',
                  'meta': {'guid': str(generate_uuid()), 'events': 100}}])
# import pdb; pdb.set_trace()
# for key, value in client.get_metadata(scope, name).iteritems():
#     print key, value
# client.set_metadata(scope, name, 'guid', generate_uuid())

