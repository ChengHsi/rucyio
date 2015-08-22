#!/usr/bin/env python

"""
AMS02 - Paramigrator4

THIS IS THE VERSION WITHOUT ALL THE HASHING BULLSHIT
parellel version of ams02-migrator
read from filelist
xrdcp to destination
at the start of each run, the finished_filelist and the exist_filelist should be consistent, not exactly the same, but at least same wc -l
"""

#
# Code goes here.
#
from multiprocessing import Process, Manager
import itertools
import sys
import os
# import hashlib
import subprocess
import shlex
# import signal
import datetime
import errno
import time
# import pdb
import argparse
from blessings import Terminal

term = Terminal()


class Writer(object):
    """Create an object with a write method that writes to a
    specific place on the screen, defined at instantiation.
    This is the glue between blessings and progressbar.
    """
    def __init__(self, location):
        """
        Input: location - tuple of ints (x, y), the position
                          of the bar in the terminal
        """
        self.location = location

    def write(self, string):
        with term.location(*self.location):
            print(string)


def write(filepath, message):
    """
    write message to filepath
    """
    # make sure that filename is just the name of the file
    if '/' in filepath:
        filename = filepath[filepath.rfind('/') + 1:]
    else:
        filename = filepath
    path = write_dir + filename
    # mkdir_p(path[:-len(filename) - 1])
    with open(path, 'a+') as file2:
        file2.write(message)


def mkdir_p(path):
    """
    same as mkdir -p
    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def timestamp():
    """
    return current time in standard time form
    """
    standard_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    return standard_time


def do_work(in_queue, out_list):
    """
    work for multiprocessing workers
    """
    while True:
        item = in_queue.get()
        line_no, line = item
        # exit signal
        if line is None:
            return
        xrdcp(line)
        # TODO: the out_list part is unessary
        out_list.append(line)


def xrdcp(line):
    """
    This line is a line from eos find -f --checksum --size [Original_path] >> [filelist]
    It will look like:
    'path=/eos/ams/Data/AMS02/2014/ISS.B950/pass6/1385485339.00000001.root size=727225390 checksum=7cf8cccd'
    """
    # Parse the line into respective attributes
    file_dict = {}
    for attr in line.split(' '):
        # Add [path, size, checksum] as key to file_dict
        file_dict[attr.split('=')[0]] = attr.split('=')[1]
    file_dict['filename'] = file_dict['path'].split('/')[-1]
    source_path = file_dict['path'].rstrip()
    source_pfn = source_prefix + source_path
    dest_path = dest_dir + file_dict['filename'].rstrip()
    dest_pfn = dest_prefix + dest_path
    cmd1 = 'xrdcp --cksum adler32:%s %s %s' % (file_dict['checksum'], source_pfn, dest_pfn)
    # cmd1 = 'xrdcp --cksum adler32:%s %s %s -f' % ('ffffffff', source_pfn, dest_pfn)
    print cmd1

    try:
        # TODO: lack a parrelell stdout interface, maybe because i am using check_all instead of Popen? thought it is neccessary for getting the duplicate exception
        subprocess.CalledProcessError = CalledProcessError
        check_output(shlex.split(cmd1), stderr=None)
    except ChecksumError:
        write('ChecksumError_filelist_' + file.split('/')[-1], line)
        pass
    except subprocess.CalledProcessError:
        write('CalledProcessError_filelist_' + file.split('/')[-1], line)
        pass
    except DestFileExist:
        xrdfs(source_path, dest_path, line)
    except:
        print sys.exc_info()[0]


def xrdfs(s_path, d_path, line):
    cmd1 = 'xrdfs %s query checksum %s' % (source_prefix, s_path)
    proc_1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_1, err_1 = proc_1.communicate()
    cmd2 = 'xrdfs %s query checksum %s' % (dest_prefix, d_path)
    proc_2 = subprocess.Popen(shlex.split(cmd2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_2, err_2 = proc_2.communicate()
    try:
        if output_1.split()[1] != output_2.split()[1]:
            write('ChecksumError_filelist_' + file.split('/')[-1], line + ' dest_checksum=' + output_2.split()[1])
        # raise ChecksumError
    except:
        write('xrdfsError_filelist_' + file.split('/')[-1], line)


def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        if retcode == 54:
            raise DestFileExist
        elif retcode == 53:
            raise ChecksumError
        else:
            raise CalledProcessError(retcode, cmd, output=output)
    return output


class CalledProcessError(Exception):
    def __init__(self, returncode, cmd, output=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d with output of %s" % (
            self.cmd, self.returncode, self.output)


class DestFileExist(Exception):
    '''File already Exists.'''
    pass


class ChecksumError(Exception):
    ''' Inconsistent Checksum between Source and Dest.'''
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('SourceFilelist', metavar='Filelist', type=str, help='Filelist')
    parser.add_argument('--dest-SE', '-S', action='store_true', help='enter destination SE for transfer e.g:tw-eos03')
    parser.add_argument('--source-prefix', '-s', action='store_true', help='enter source-prefix for transfer e.g: root://hp-disk1.gridi.sinica.edu.tw, default is set as root://eosams.cern.ch')
    parser.add_argument('--dest-dir', '-d', action='store_true', help='enter destination diractory of the transfer. e.g: /eos/ams/amsdatadisk/2014/ISS.B950/pass6/')

    args = parser.parse_args()
    file = str(sys.argv[1])
    write_dir = '/'.join(file.split('/')[:-1]) + '/result/'
    try:
        destSE = args.dest_SE
    except:
        raise Exception('target SE is missing!')
    try:
        source_prefix = args.source_prefix
    except:
        source_prefix = 'root://eosams.cern.ch/'
    dest_prefix = 'root://%s.grid.sinica.edu.tw/' % (destSE)
    try:
        dest_dir = args.dest_dir
    except:
        raise Exception('Destination Directory is missing!')
        # dest_dir = '/eos/ams/amsdatadisk/2014/ISS.B950/pass6/'
    num_workers = 1

    manager = Manager()
    results = manager.list()
    work = manager.Queue(num_workers)

    # start for workers
    pool = []
    for i in xrange(num_workers):
        p = Process(target=do_work, args=(work, results))
        p.start()
        pool.append(p)
    # produce data
    with open(file) as f:

        iters = itertools.chain(f, (None,) * num_workers)
        for num_and_line in enumerate(iters):
            # num_and_line is a tuple, Ex: (0, '1383594243.00000001.root\n') or (0, 'path=/eos/ams/Data/AMS02/2014/ISS.B950/pass6/1385485339.00000001.root size=727225390 checksum=7cf8cccd'\n)
            # pdb.set_trace()
            work.put(num_and_line)

    print 'finished'
