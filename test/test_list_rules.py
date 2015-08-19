'''
This is a script to test the difference of list-dids and list-rules
'''

from rucio.db import models
from rucio.db.session import read_session, transactional_session, stream_session
from rucio.db.constants import DIDType
from rucio.common import exception
from rucio.client.didclient import DIDClient
dc = DIDClient()
import sys
# del sys.modules['rucio']
# # import imp
# # rucio = imp.load_source('rucio','/opt/rucio/lib/rucio/__init__.py')
filename = sys.argv[1]

for x in dc.list_did_rules('ams-user-chenghsi', filename):
    print x[u'name']
# print get_did('ams-user-chenghsi', 'd2')
# dc.detach_dids('ams-user-chenghsi', 'd1', ['file3'])

# print non_attached('ams-user-chenghsi', ['file1', 'file2', 'file3', 'file4'])





