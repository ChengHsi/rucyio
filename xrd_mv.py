import shlex
import subprocess
import argparse

parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('SourceFilelist', metavar='Filelist', type=str, help='Filelist')
parser.add_argument('--source-SE', '-S', metavar='Sour-SE', type=str, help='enter source SE for transfer e.g:tw-eos03')
parser.add_argument('--dest-prefix', '-d', metavar='dest-Prefix', type=str, help='enter dest-prefix for transfer e.g: /eos/ams/amsdatadisk/2011B/ISS.B620/')
args = parser.parse_args()
file = args.SourceFilelist

with open(file, 'rw') as f:
    for line in f:
        filename = line.split('/')(-1)
        dest = args.dest_prefix + filename
        cmd = 'xrd %s mv %s %s' %(args.source_SE, line, dest)
        print cmd
        break

