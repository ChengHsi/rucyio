import shlex
import os
import sys
import subprocess
import argparse
from ams02_paramigrator5 import check_output as check_output


parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('SourceFilelist', metavar='Filelist', type=str, help='Filelist')
parser.add_argument('--source-SE', '-S', metavar='Sour-SE', type=str, help='enter source SE for transfer e.g:tw-eos03')
parser.add_argument('--dest-prefix', '-d', metavar='dest-Prefix', type=str, help='enter dest-prefix for transfer e.g: /eos/ams/amsdatadisk/2011B/ISS.B620/')
args = parser.parse_args()
file = args.SourceFilelist
if args.source_SE.startswith('tw'):
    source = args.source_SE + '.grid.sinica.edu.tw'
with open(file, 'rw') as f:
    for line in f:
        filename = line.split('/')[-1]
        dest = args.dest_prefix + filename
        cmd = 'xrd %s mv %s %s' %(source, line, dest)
        check_output(shlex.split(cmd), stderr=None)
        print cmd

