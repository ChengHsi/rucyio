"""
Register Exist Files

Take a list of dictionaries of files that exist on SE,
add to Rucio DB.
Should be a taking a list of JSON files instead?
"""

from rucio.common.utils import generate_uuid
####from client####
from rucio.client.replicaclient import ReplicaClient
repCli = ReplicaClient()
import sys, datetime
from rucio.client.didclient import DIDClient
didCli = DIDClient()
from rucio.client.ruleclient import RuleClient
ruleCli = RuleClient()
from rucio.client.rseclient import RSEClient
rseCli = RSEClient()
from rucio.common import exception

argv_file = str(sys.argv[1])
with open(argv_file, 'r') as dids:
    for did in dids:
        did = did.rstrip('\n')
        did_list = did.split(' ')
        if ':' in did[0]:
            scope = did_list[0][0]
            filename = did_list[0][1]
        else:
            filename = unicode(did_list[0])
            scope = 'ams-user-testuser1'
        # rse_name = 'TW-EOS00_AMS02DATADISK'
        rse_name = 'AMS-EOS00_AMS02DATADISK'
        prefix = '/eos/ams/amsdatadisk/'
        adler32 = did_list[1]
        bytes = int(did_list[2])
        md5 = unicode(did_list[3])
        pfn = prefix + scope + '/' + filename
        ##for files already with replicas:
        #for x in repCli.list_replicas([{'scope': scope, 'name': filename}]):
        #    adler32 = x['adler32']
        #    md5 = x['md5']
        #    bytes = x['bytes']
        ##    print x
        # file_meta = didCli.get_metadata(scope, filename)
        file_meta = {}
        # file_meta =  didCli.get_metadata(test_did.split(':')[0], test_did.split(':')[1])
        file_meta['adler32'] = adler32
        file_meta['scope'] = scope
        file_meta['name'] = filename
        file_meta['bytes'] = bytes
        file_meta['md5'] = md5
        file_meta['guid'] = str(generate_uuid())
        #repCli.delete_replicas(rse_name, [{'scope': scope, 'name': filename}])

        try:
            repCli.add_replica(rse_name, scope, filename, bytes, adler32,pfn, md5, file_meta)
        except exception.Duplicate:
            print 'already replicated, but adding rules'
            ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1, \
            rse_expression=rse_name, grouping='DATASET')
            continue
        ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1, \
        rse_expression=rse_name, grouping='DATASET')

        print 'after add:'
        for x in repCli.list_replicas([{'scope': scope, 'name': filename}]):
            print x
###################################################
#for x in rseCli.list_rses('TW-EOS01_AMS02DATADISK'):
#    print x
#rseCli.delete_rse(rse_name)
#print rseCli.get_rse(rse_name)
#for x in rseCli.list_rses():
#    print x
#rseCli.delete_protocols(rse_name, 'xrootd')
#print rseCli.list_rse_attributes(rse_name)
#print rseCli.get_protocols(rse_name)
#from rucio.api.rse import del_rse, get_rse, get_protocols
#del_rse(rse_name, 'root')
