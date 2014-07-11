####from client####
from rucio.client.replicaclient import ReplicaClient
rep = ReplicaClient()
print 'before:'
for x in rep.list_replicas([{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}]):
    print x
rep.delete_replicas('TW-EOS00_AMS02DATADISK', [{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}])
print 'after deletion:'
for x in rep.list_replicas([{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}]):
    print x
rep.add_replica('TW-EOS00_AMS02DATADISK', 'twgrid-user-testuser1', '7580695258.35842516.root', 15, '29ae0489', pfn='/eos/ams/amsdatadisk/twgrid-user-testuser1/ee/c6/7580695258.35842516.root')
print 'after add:'
for x in rep.list_replicas([{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}]):
    print x
###################
#from rucio.rse import rsemanager as rsemgr
#from rucio.core import replica
#for x in replica.list_replicas([{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}]):
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
#print rsemgr.get_rse_info('RUCIO-DPM01_TWGRIDSCRATCHDISK')i
#from rucio.api.replica import add_replicas as add
#add('TW-EOS00_AMS02DATADISK', [{'scope': 'twgrid-user-testuser1', 'name': '7580695258.35842516.root'}], 'root')
