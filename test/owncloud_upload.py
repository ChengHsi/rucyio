'''
Owncloud upload script
This is a striped version of rucio upload, specific for uploading to an owncloud rse.
'''
from rucio.client.client import Client
from rucio.common.utils import adler32, execute, generate_uuid
from rucio.common import exception
from rucio.rse import rsemanager as rsemgr

import argparse
import sys
import os

def owncloud_pfn(rse, name, fscope):
    '''
    Return a owncloud specific PFN
    e.g.: xroot://owncloud-eos-mgm.twgrid.org:1094//eos/user/c/chenghsi/blah
    rse: name of rse
    name: source filepath
    fscope: scope of file. should be *-user-(username)
    '''
    rse_settings = rsemgr.get_rse_info(rse)
    protocol = rse_settings['protocols'][0]
    if 'user' in fscope:
        username = fscope.split('-')[-1]
        additional_prefix = '%s/%s' %(username[0], username)
    return '%s://%s:%s/%s%s/%s' % (protocol['scheme'], protocol['hostname'], protocol['port'], protocol['prefix'], additional_prefix, os.path.basename(name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True,  description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--scope', '-s', metavar='scope', type=str, help='Scope of the file to register to. e.g:ams-user-chenghsi')
    parser.add_argument('--rse', metavar='rse', type=str, help='Target RSE of the filelist, e.g: OWNCLOUD_TESTBED_SCRATCHDISK')
    parser.add_argument('Filename', metavar='Filename', type=str, help='Source File to upload.')
    args = parser.parse_args()
    client = Client()
    name = args.Filename #Actually, this is source_url
    directory = os.path.dirname(name)
    if args.rse:
        rse = args.rse
    else:
        rse = 'OWNCLOUD_TESTBED_SCRATCHDISK'
        # rse = 'EOS01_OWNCLOUD_SCRATCHDISK'
    fscope = args.scope if args.scope else 'ams-user-chenghsi'
    rse_settings = rsemgr.get_rse_info(rse)
    checksum = adler32(name)
    size = os.stat(name).st_size
    list_files = []
    list_files.append({'scope': fscope, 'name': os.path.basename(name), 'bytes': size, 'adler32': checksum, 'state': 'A', 'meta': {'guid': generate_uuid()}, 'pfn': owncloud_pfn(rse, name, fscope)},)
    for f in list_files:
        client.add_replicas(files=[f], rse=rse)
        client.add_replication_rule([f], copies=1, rse_expression=rse)
        rsemgr.upload(rse_settings=rse_settings, lfns=[{'name': f['name'], 'scope': f['scope'], 'adler32': f['adler32'], 'filesize': f['bytes']}], source_dir=directory)
