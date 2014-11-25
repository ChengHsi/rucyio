from rucio.common.utils import generate_uuid
####from client####
from rucio.client.replicaclient import ReplicaClient
repCli = ReplicaClient()
#did = 'ams-2011B-ISS.B620-pass4:1368923945.00000001.root'
test_did = 'twgrid-user-testuser1:chtest1'
import sys, datetime
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
        # print did
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
        print filename, adler32, bytes
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
        #print 'after deletion:'
        #for x in rep.list_replicas([{'scope': scope, 'name': filename}]):
        #    print x

        # dt = 'datetime.datetime(' + str(datetime.datetime.utcnow().strftime('%Y, %m, %d, %H, %M, %S')) + ')'
        # dt = None
        # file_meta = {'campaign': None, 'is_new': True, 'is_open': None, 'guid': None, 'availability': None, 'deleted_at': None, 'panda_id': None, 'version': None, 'scope': scope, 'hidden': False, 'md5': None, 'events': None, 'adler32': adler32, 'complete': None, 'monotonic': False, 'updated_at': dt, 'obsolete': False, 'did_type': 'FILE', 'suppressed': False, 'expired_at': None, 'stream_name': None, 'account': 'root', 'run_number': None, 'name': filename, 'task_id': None, 'datatype': None, 'created_at': dt, 'bytes': int(bytes), 'project': None, 'length': None, 'prod_step': None} 
        try:
            import pdb;pdb.set_trace()
            repCli.add_replica(rse_name, scope, filename, bytes, adler32,pfn, md5, file_meta)
            # didCli.set_metadata(scope, scope+filename, 'updated_at', 'datetime.datetime(' + str(datetime.datetime.utcnow().strftime('%Y, %m, %d, %H, %M, %S')) + ')')
            # didCli.set_metadata(scope, scope+filename, 'created_at', 'datetime.datetime(' + str(datetime.datetime.utcnow().strftime('%Y, %m, %d, %H, %M, %S')) + ')')
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
