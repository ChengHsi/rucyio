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
import shlex
# import signal
import datetime
import errno
import time


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
    source_pfn = source_prefix + file_dict['path'].rstrip()
    dest_pfn = dest_prefix + dest_dir + file_dict['filename'].rstrip()
    cmd1 = 'xrdcp --cksum adler32:%s %s %s' % (file_dict['checksum'], source_pfn, dest_pfn)
    # cmd1 = 'xrdcp --cksum adler32:%s %s %s -f' % ('ffffffff', source_pfn, dest_pfn)
    print cmd1

    try:
        # TODO: lack a parrelell stdout interface, maybe because i am using check_all instead of Popen? thought it is neccessary for getting the duplicate exception
        # overwrite CalledProcessError due to `output` keyword might be not available
        subprocess.CalledProcessError = CalledProcessError
        subprocess.check_call(shlex.split(cmd1), stdout=None, stderr=None)
        # sp = subprocess.Popen(shlex.split(cmd1), stdout=None, stderr=subprocess.PIPE).wait()
        # write('finished_filelist_' + file.split('/')[-1], line)
        # out, err = sp.communicate()
        # print out
        # if out:
        #     print "standard output of subprocess:"
        #     print out
        #if err:
        #     print "standard error of subprocess:"
        #     print err
        #     if 'File exists' in err:
        #         raise DestFileExist('File already exist')
        #     if '[ERROR] CheckSum error' in err:
        #         raise ChecksumError('This is HUGE')

        # print "returncode of subprocess:"
        # print sp.returncode
    except subprocess.CalledProcessError:
        # Checksum, Exist
        # print subprocess.PIPE
        pass
        # print 'CalledProcessError'
    except DestFileExist:
        print '%s already exists at %s' %(file_dict['filename'], dest_pfn)
        pass
    except ChecksumError:
        write('error_filelist_' + file.split('/')[-1], line)
        print 'ChecksumError'
        pass
    except:
        print sys.exc_info()[0]

class CalledProcessError(Exception):
    def __init__(self, returncode, cmd, output=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
    def __str__(self):
        return "Command '%s' returned non-zero exit status %d with output of %s" % (
            self.cmd, self.returncode, self.output)

class DestFileExist(Exception):
    pass

class ChecksumError(Exception):
    pass

if __name__ == "__main__":
    file = str(sys.argv[1])
    write_dir = '/'.join(file.split('/')[:-1]) + '/result/'
    try:
        destSE = str(sys.argv[2])
    except:
        destSE = 'tw-eos03'

    source_prefix = 'root://eosams.cern.ch/'
    dest_prefix = 'root://%s.grid.sinica.edu.tw/' % (destSE)
    dest_dir = '/eos/ams/amsdatadisk/2014/ISS.B950/pass6/'
    num_workers = 64

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
            # import pdb; pdb.set_trace()
            work.put(num_and_line)

    print 'finished'
