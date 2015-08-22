from rucio.client.client import Client
from rucio.common.utils import adler32, execute
from rucio.common import exception

import sys
import os
client = Client()
# scope = sys.argv[1]
source_url = sys.argv[1]
name = source_url.split('/')[-1]
rse = 'OWNCLOUD_TESTBED_SCRATCHDISK'
scope = 'ams-user-chenghsi'
checksum = adler32(source_url)
bytes = os.stat(source_url).st_size
path= '/eos/user/c/chenghsi/' + name
pfn = 'xroot://owncloud-eos-mgm.twgrid.org:1094/' + path
try:
    cmd = 'xrdcp -f %s %s' % (source_url, pfn)
    # status, out, err = execute(cmd, env=self.execenv)
    import pdb; pdb.set_trace()
    status, out, err = execute(cmd)
    if not status == 0:
        raise exception.RucioException(err)
    client.add_replica(rse, scope, name, bytes, checksum, pfn, md5=None, meta={})
    for x in client.list_replicas([{'scope':scope, 'name':name}]):
        print x
        client.add_replication_rule([x], copies=1, rse_expression=rse)
except Exception as e:
    raise exception.ServiceUnavailable(e)

