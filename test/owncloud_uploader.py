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


class OwncloudUploader(object):
    def __init__(self, scope, rse, filename):
        self.fscope = scope if scope else 'ams-user-chenghsi'
        self.rse = rse if rse else 'OWNCLOUD_TESTBED_SCRATCHDISK'
        self.name = filename
    def owncloud_pfn(self):
        '''
        Return a owncloud specific PFN
        e.g.: xroot://owncloud-eos-mgm.twgrid.org:1094//eos/user/c/chenghsi/blah
        rse: name of rse
        name: source filepath
        fscope: scope of file. should be *-user-(username)
        '''
        self.rse_settings = rsemgr.get_rse_info(self.rse)
        protocol = self.rse_settings['protocols'][0]
        if 'user' in self.fscope:
            username = self.fscope.split('-')[-1]
            additional_prefix = '%s/%s' %(username[0], username)
        else:
            raise Exception('I don\'t think you have the right scope: %s'  %(self.fscope))
        return '%s://%s:%s/%s%s/%s' % (protocol['scheme'], protocol['hostname'], protocol['port'], protocol['prefix'], additional_prefix, os.path.basename(self.name))
    def make_file_list(self):
        '''
        Return a list of file's specs in dictionary form to be uploaded.
        '''
        self.checksum = adler32(self.name)
        self.size = os.stat(self.name).st_size
        self.client = Client()
        self.directory = os.path.dirname(self.name)
        list_files = []
        list_files.append({'scope': self.fscope, 'name': os.path.basename(self.name), 'bytes': self.size, 'adler32': self.checksum, 'state': 'A', 'meta': {'guid': generate_uuid()}, 'pfn': self.owncloud_pfn()},)
        return list_files
    def upload(self):
        '''
        A upload function to register the file into rucio.
        '''
        for f in self.make_file_list():
            self.client.add_replicas(files=[f], rse=self.rse)
            self.client.add_replication_rule([f], copies=1, rse_expression=self.rse)
            rsemgr.upload(rse_settings=self.rse_settings, lfns=[{'name': f['name'], 'scope': f['scope'], 'adler32': f['adler32'], 'filesize': f['bytes']}], source_dir=self.directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True,  description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--scope', '-s', metavar='scope', type=str, help='Scope of the file to register to. e.g:ams-user-chenghsi')
    parser.add_argument('--rse', metavar='rse', type=str, help='Target RSE of the filelist, e.g: OWNCLOUD_TESTBED_SCRATCHDISK')
    parser.add_argument('filename', metavar='Filename', type=str, help='Source File to upload.')
    args = parser.parse_args()
    ou = OwncloudUploader(**vars(args))
    ou.upload()
