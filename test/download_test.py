import requests
import os
import urlparse
import urllib
import json
import requests

import boto
import boto.s3.connection
# import webdav

from boto.s3.key import Key

from rucio.common import exception
from rucio.common.config import get_rse_credentials

from exceptions import NotImplementedError
from rucio.rse.protocols import protocol
from urlparse import urlparse
import xml.etree.ElementTree as ET

from progressbar import ProgressBar
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from sys import stdout
from xml.parsers import expat

path = 'https://192.168.20.101:9000/1000_genome_exome/HG00234.alt_bwamem_GRCh38DH.20150826.GBR.exome.cram'
cert = ('/tmp/x509up_u500_amspil', '/tmp/x509up_u500_amspil')
dest = u'./NoProjectDefined/HG00234.alt_bwamem_GRCh38DH.20150826.GBR.exome.cram.part'
chunksize = 1024

result = requests.Session().get(path, verify=False, stream=True, timeout=300, cert=cert)
if result and result.status_code in [200, ]:
    length = None
    if 'content-length' in result.headers:
        length = int(result.headers['content-length'])
        totnchunk = int(length / chunksize) + 1
    with open(dest, 'wb') as f:
        nchunk = 0
        try:
            if length:
                pbar = ProgressBar(maxval=totnchunk).start()
            else:
                print 'Malformed HTTP response (missing content-length. Cannot show progress bar.'
            # import pdb; pdb.set_trace()
            for chunk in result.iter_content(chunksize):
                f.write(chunk)
                if length:
                    nchunk += 1
                    pbar.update(nchunk)
        finally:
            if length:
                pbar.finish()
