#!/usr/bin/env python

"""
AMS02 - Paramigrator3

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
# import shlex
# import signal
import datetime
import errno
import time
# import pdb


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
        compare_filelist(line)
        # TODO: the out_list part is unessary
        out_list.append(line)


def parse_line(line):
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
    # source_path = file_dict['path'].rstrip()
    # source_pfn = source_prefix + source_path
    # dest_path = dest_dir + file_dict['filename'].rstrip()
    # dest_pfn = dest_prefix + dest_path
    return file_dict


def compare_filelist(line):
    compare_this_dict = parse_line(line)
    for filename in compare_this_dict['filename']:
        if filename in checksum_dict.keys():
            if compare_this_dict['checksum'] != checksum_dict[filename]:
                write('ChecksumError_filelist_' + file.split('/')[-1], line)


def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popens(stdout=subprocess.PIPE, *popenargs, **kwargs)
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
    bigFile = str(sys.argv[1])
    smallFile = str(sys.argv[2])
    write_dir = '/'.join(bigFile.split('/')[:-1]) + '/result/'
    checksum_dict = {}
    with open(smallFile, 'r') as small:
        for line in small:
            parse_line(line)
            checksum_dict[parse_line['filename']] = parse_line['checksum']

    # source_prefix = 'root://eosams.cern.ch/'
    # dest_prefix = 'root://%s.grid.sinica.edu.tw/' % (destSE)
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
    with open(bigFile) as f:

        iters = itertools.chain(f, (None,) * num_workers)
        for num_and_line in enumerate(iters):
            # num_and_line is a tuple, Ex: (0, '1383594243.00000001.root\n') or (0, 'path=/eos/ams/Data/AMS02/2014/ISS.B950/pass6/1385485339.00000001.root size=727225390 checksum=7cf8cccd'\n)
            # pdb.set_trace()
            work.put(num_and_line)

    print 'finished'
