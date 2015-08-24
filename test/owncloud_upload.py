from rucio.client.client import Client
from rucio.common.utils import adler32, execute, generate_uuid
from rucio.common import exception
from rucio.rse import rsemanager as rsemgr

import sys
import os

def owncloud_pfn(rse, name):
    '''
    rse: name of rse
    name: source filepath
    '''
    rse_settings = rsemgr.get_rse_info(rse)
    protocol = rse_settings['protocols'][0]
    return '%s://%s:%s/%s/%s' % (protocol['scheme'], protocol['hostname'], protocol['port'], protocol['prefix'], os.path.basename(name))

if __name__ == '__main__':
    client = Client()
    name = sys.argv[1] #Actually, this is source_url
    directory = os.path.dirname(name)
    rse = 'OWNCLOUD_TESTBED_SCRATCHDISK'
    # rse = 'EOS01_OWNCLOUD_SCRATCHDISK'
    rse_settings = rsemgr.get_rse_info(rse)
    fscope = 'ams-user-chenghsi'
    checksum = adler32(name)
    size = os.stat(name).st_size
    # path = '/eos/user/c/chenghsi/' + os.path.basename(name)
    # pfn = 'xroot://owncloud-eos-mgm.twgrid.org:1094/' + path
    list_files = []
    list_files.append({'scope': fscope, 'name': os.path.basename(name), 'bytes': size, 'adler32': checksum, 'state': 'A', 'meta': {'guid': generate_uuid()}, 'pfn': owncloud_pfn(rse, name)},)
    for f in list_files:
        client.add_replicas(files=[f], rse=rse)
        client.add_replication_rule([f], copies=1, rse_expression=rse)
        rsemgr.upload(rse_settings=rse_settings, lfns=[{'name': f['name'], 'scope': f['scope'], 'adler32': f['adler32'], 'filesize': f['bytes']}], source_dir=directory)
    # try:
    #     cmd = 'xrdcp -f %s %s' % (name, pfn)
    #     # status, out, err = execute(cmd, env=self.execenv)
    #     import pdb; pdb.set_trace()
    #     status, out, err = execute(cmd)
    #     if not status == 0:
    #         raise exception.RucioException(err)
    #     client.add_replicas(files=[f], rse=rse)
    #     for x in client.list_replicas([{'scope':scope, 'name':name}]):
    #         print x
    #         client.add_replication_rule([x], copies=1, rse_expression=rse)
    # except Exception as e:
    #     raise exception.ServiceUnavailable(e)
