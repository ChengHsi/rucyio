####from client####
from rucio.client.replicaclient import ReplicaClient
repCli = ReplicaClient()
#did = 'ams-user-chenghsi:Acceptance_Form.jpg'.split(':')
#did = 'ams-2011B-ISS.B620-pass4:1368923945.00000001.root'
import sys
from rucio.client.didclient import DIDClient
didCli = DIDClient()
from rucio.client.ruleclient import RuleClient
ruleCli = RuleClient()
from rucio.client.rseclient import RSEClient
rseCli = RSEClient()
from rucio.common import exception
argv_file =str(sys.argv[1])
with open(argv_file, 'r') as dids:
    for did in dids:
        did = did.rstrip('\n')
        print did
        did_list = did.split(':')
        scope = did_list[0]
        filename = did_list[1]
        rse_name = 'TW-EOS01_AMS02DATADISK'
        adler32 = ''
        md5 = ''
        bytes = 0
        #print 'before:'
        for x in repCli.list_replicas([{'scope': scope, 'name': filename}]):
            adler32 = x['adler32']
            md5 = x['md5']
            bytes = x['bytes']
        #    print x
        file_meta = didCli.get_metadata(scope, filename) 
        ##repCli.delete_replicas(rse_name, [{'scope': scope, 'name': filename}])
        ##print 'after deletion:'
        ##for x in rep.list_replicas([{'scope': scope, 'name': filename}]):
        ##    print x
        try:
            repCli.add_replica(rse_name, scope, filename, bytes, adler32, md5, file_meta)
        except exception.Duplicate:
            print 'already replicated, but adding rules'
            ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1, \
            rse_expression=rse_name, grouping='DATASET')
            continue
        ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1, \
        rse_expression=rse_name, grouping='DATASET')
        
        #print 'after add:'
        #for x in repCli.list_replicas([{'scope': scope, 'name': filename}]):
        #    print x
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
#print get_rse(rse_name)
#print get_rse('TW-DPM01_AMS02DATADISK')
#print get_rse('TW-DPM01_TWGRIDSCRATCHDISK')
#print get_rse('TW-DPM01_TWGRIDARCHIVE')
#print get_rse('TW-DPM01_AMS02SCRATCHDISK')
#print get_protocols(rse_name, 'root')
##################################################
#from rucio.rse import rsemanager as rsemgr
#from rucio.core import replica
#for x in replica.list_replicas([{'scope': scope, 'name': filename}]):
#    print x
##################################################
#from rucio.rse import rsemanager as rsemgr
#from dogpile.cache import make_region
#def rse_key_generator(namespace, fn, **kwargs):
#    def generate_key(rse, session=None):
#        return rse
#    return generate_key
#
## Preparing region for dogpile.cache
#rse_region = make_region(function_key_generator=rse_key_generator).configure(
#    'dogpile.cache.memory',
#    expiration_time=3600,
#)
#
#print rsemgr.get_rse_info(rse_name)
#print rsemgr.get_rse_info('TW-DPM01_AMS02SCRATCHDISK')
#from rucio.api.replica import add_replicas as add
#add(rse_name, [{'scope': scope, 'name': filename}], 'root')
