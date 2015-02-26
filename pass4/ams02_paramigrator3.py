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
import hashlib
import subprocess
import shlex
import signal
import datetime
import errno
import time


def xrdcp(line):
    """
    """
    ori_path = 'root://eosams.cern.ch//eos/ams/Data/AMS02/2014/ISS.B950/pass6/%s' % line.rstrip()
    line_struct = line.split('/')
    # print line[-1]
    # ori_path = 'root://tw-eos01.grid.sinica.edu.tw/%s' % line.rstrip()
    dest_path = 'root://%s.grid.sinica.edu.tw/%s' % (destSE, '/eos/ams/amsdatadisk/tw-eos01-pass4/'+line_struct[-1].rstrip())
    # dest_path = 'root://%s.grid.sinica.edu.tw/%s' % (destSE, hash(scope, line, rse_prefix))
    cmd1 = 'xrdcp %s %s' % (ori_path, dest_path)
    print cmd1

    try:
        # TODO: lack a parrelell stdout interface, maybe because i am using check_all instead of Popen? thought it is neccessary for getting the duplicate exception
        subprocess.check_call(shlex.split(cmd1), stdout=None, stderr=None)
        write('finished_filelist', line)
    except subprocess.CalledProcessError:
        pass
    except:
        print sys.exc_info()[0]
        raise


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


if __name__ == "__main__":
    manager = Manager()
    file = str(sys.argv[1])
    file_struct = file.split('/')
    # split_input(file)
    # scope = 'ams-2011B-ISS.B620-pass4'
    rse_prefix = '/eos/ams/amsdatadisk/'
    # scope = 'protons.B620dev'
    current_line = None
    write_dir = '/root/chchao/rucyio/pass4/result/'
    num_workers = 128 
    try:
        destSE = str(sys.argv[2])
    except:
        destSE = 'tw-eos03'

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
            # num_and_line is a tuple
            # Example:
            # (0, '1383594243.00000001.root\n')
            work.put(num_and_line)

    print 'finished'
