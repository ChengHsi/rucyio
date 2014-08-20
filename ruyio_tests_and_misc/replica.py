####from client####
from rucio.client.replicaclient import ReplicaClient
rep = ReplicaClient()
#did = 'ams-user-chenghsi:Acceptance_Form.jpg'.split(':')
did = 'ams-2011B-ISS.B620-pass4:1368923945.00000001.root'
#did = 'ams-2011B-ISS.B620-pass4:2011-06-14'
did_list = did.split(':')
scope = did_list[0]
filename = did_list[1]
rse_name = 'TW-EOS01_AMS02DATADISK'
adler32 = ''
md5 = ''
bytes = 0
#print 'before:'
for x in rep.list_replicas([{'scope': scope, 'name': filename}]):
    adler32 = x['adler32']
    md5 = x['md5']
    bytes = x['bytes']
    print adler32, md5, bytes
#from rucio.client.didclient import DIDClient
#did = DIDClient()
#file_meta = did.get_metadata(scope, filename) 
#rep.delete_replicas(rse_name, [{'scope': scope, 'name': filename}])
#print 'after deletion:'
#for x in rep.list_replicas([{'scope': scope, 'name': filename}]):
#    print x
#rep.add_replica(rse_name, scope, filename, bytes, adler32, md5, file_meta)
print 'test'
#print 'after add:'
#for x in rep.list_replicas([{'scope': scope, 'name': filename}]):
#    print x
###################################################
from rucio.client.ruleclient import RuleClient
rule = RuleClient()
from rucio.client.rseclient import RSEClient
rse = RSEClient()
#for x in rse.list_rses('TW-EOS01_AMS02DATADISK'):
#    print x
#rse.delete_rse(rse_name)
#print rse.get_rse(rse_name)
#for x in rse.list_rses():
#    print x
#rse.delete_protocols(rse_name, 'xrootd')
#print rse.list_rse_attributes(rse_name)
##print rse.get_protocols(rse_name)
#from rucio.api.rse import del_rse, get_rse, get_protocols
##del_rse(rse_name, 'root')
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
###################
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
