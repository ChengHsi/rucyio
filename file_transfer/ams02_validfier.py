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
    global counter
    compare_this_dict = parse_line(line)
    print 'Checking if %s in smaller file:' % (compare_this_dict['filename'])
    filename = compare_this_dict['filename']
    if filename in checksum_dict.keys():
        print 'Yes'
        if compare_this_dict['checksum'] != checksum_dict[filename]:
            print 'Also it has a different checksum.'
            write('ChecksumError_' + bigFile.split('/')[-1] + '_' + smallFile.split('/')[-1], line)
            counter = counter + 1

<<<<<<< HEAD:pass4/ams02_paramigrator3_test.py
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
        pass
        # xrdfs(source_path, dest_path, line)
    except:
        print sys.exc_info()[0]


def xrdfs(s_path, d_path, line):
    cmd1 = 'xrdfs %s query checksum %s' % (source_prefix, s_path)
    proc_1 = subprocess.Popen(shlex.split(cmd1), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_1, err_1 = proc_1.communicate()
    cmd2 = 'xrdfs %s query checksum %s' % (dest_prefix, d_path)
    proc_2 = subprocess.Popen(shlex.split(cmd2), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_2, err_2 = proc_2.communicate()
    if output_1.split()[1] != output_2.split()[1]:
        write('ChecksumError_filelist_' + file.split('/')[-1], line + ' dest_checksum=' + output_2.split()[1])
        # raise ChecksumError
=======
    else:
        print 'No'
>>>>>>> d0d48cc12a4e09d321a718d2a6bd67036fec32e9:file_transfer/ams02_validfier.py


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
<<<<<<< HEAD:pass4/ams02_paramigrator3_test.py
    file = str(sys.argv[1])
    write_dir = '/'.join(file.split('/')[:-1]) + '/result/'
    try:
        destSE = str(sys.argv[2])
    except:
        destSE = 'tw-eos03'

    source_prefix = 'root://hp-disk1.grid.sinica.edu.tw/'
    dest_prefix = 'root://%s.grid.sinica.edu.tw/' % (destSE)
    dest_dir = '/eos/ams/amsdatadisk/Data/ISS.B950R/pass6/nt/root/'
    num_workers = 1 
=======
    counter = 0
    bigFile = str(sys.argv[1])
    smallFile = str(sys.argv[2])
    write_dir = '/'.join(bigFile.split('/')[:-1]) + '/result/'
    print 'write_dir is:', write_dir
    checksum_dict = {}
    with open(smallFile, 'r') as small:
        for line in small:
            linedict = parse_line(line)
            checksum_dict[linedict['filename']] = linedict['checksum']
        # print checksum_dict['1313645806.00000001.root']

    # source_prefix = 'root://eosams.cern.ch/'
    # dest_prefix = 'root://%s.grid.sinica.edu.tw/' % (destSE)
    # dest_dir = '/eos/ams/amsdatadisk/2014/ISS.B950/pass6/'
    num_workers = 128
>>>>>>> d0d48cc12a4e09d321a718d2a6bd67036fec32e9:file_transfer/ams02_validfier.py

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
            work.put(num_and_line)

    print 'Checksum Errors found:', counter
