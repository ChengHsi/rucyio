#!/usr/bin/env python

"""
AMS02 - Paramigrator

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
from blessings import Terminal


def hash(scope, ori_line, rse_prefix):
    """
    scope: ams-MC-2011B-protons.B620dev-pl1.flux.ecal.204000
    ori_line: /eos/ams/MC/AMS02/2011B/protons.B620dev/pr.pl1.2004000/1208288289.00000001.root
    pfn: /eos/ams/amsscratchdisk/MC/2011B/protons.B620dev/pl1.flux.ecal.204000/62/b1/file1_1
    """
    scope_pos = ori_line.find('protons.B620dev')
    data_struct = ori_line[scope_pos:].split('/')
    scope_struct = ''
    for struct in data_struct[:-1]:
        scope_struct += ('/' + struct)

    hstr = hashlib.md5('%s:%s' % (scope, ori_line)).hexdigest()
    return rse_prefix + 'MC/2011B' + scope_struct + '/%s/%s/%s' % (hstr[0:2], hstr[2:4], data_struct[-1].rstrip())

    # hstr = hashlib.md5('%s:%s' % (scope, ori_line)).hexdigest()
    # return '/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/' + '%s/%s/%s' % (hstr[0:2], hstr[2:4], ori_line.rstrip())


# def read(file):
#     """file
#     readline from file,
#     xrdcp to destination
#     """
#     with open(file, 'r') as file1:
#         for line in file1:
#             global current_line
#             current_line = line
#             xrdcp(line)


def xrdcp(line):
    """
    """
    # ori_path = 'root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/%s' % line.rstrip()
    ori_path = 'root://eosams.cern.ch/%s' % line.rstrip()
    dest_path = 'root://%s.grid.sinica.edu.tw/%s' % (destSE, hash(scope, line, rse_prefix))
    # cmd1 = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select cp --checksum ori_path dest_path'
    cmd1 = 'xrdcp %s %s' % (ori_path, dest_path)
    print cmd1

    try:
        # TODO: lack a parrelell stdout interface, maybe because i am using check_all instead of Popen? thought it is neccessary for getting the duplicate exception
        subprocess.check_call(shlex.split(cmd1), stdout=None, stderr=None)
        # print sub1.stdin
        # subprocess.Popen(shlex.split(cmd1), stdout=None, stderr=None)
        print '\n %s finished. \n' % (line.rstrip())
        # sub = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        # while sub.poll() is None:
        #    l = sub.stdout.readline()  # This blocks until it receives a newline.
        #    print l
        # When the subprocess terminates print unconsumed output and write to finished_filelist
        # print sub.stdout.read()
        write('finished_filelist', line)
    except subprocess.CalledProcessError:
        # In the case of duplicate file
        # TODO: this is not exactly a well defined catching, to general
        # cmd2 = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select fileinfo %s --checksum' % ori_path
        # subprocess.Popen(cmd2)
        # cmd3 = '/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select fileinfo %s --checksum' % dest_path
        # subprocess.Popen(cmd3)
        # write('exist_filelist', line)
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


def sighandler(signum, frame):
    """
    handles sig caught from signal_trapper
    """
    message = 'caught signal ' + str(signum) + ' at: ' + timestamp() + '\n' + str(current_line) + '\n'
    write(str(timestamp()[:10]) + '/sighandler_result', message)
    sys.exit(1)


def signal_trapper():
    """
    trap all caughtable signal through sighandler
    """
    for i in [x for x in dir(signal) if x.startswith("SIG")]:
        try:
            signum = getattr(signal, i)
            signal.signal(signum, sighandler)
        except RuntimeError as e:
            sighandler(e, None)
        except ValueError:
            pass


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
        # finished = write_dir + 'finished_filelist'
        # exist = write_dir + 'exist_filelist'
        # with open(exist, 'r') as exists:
        #     in_file = False
        #     for exists_line in exists:
        #         print exists_line
        #         if line in exists_line:
        #             print 'Found!'
        #             in_file = True
        #             break
        #     if not in_file:
        xrdcp(line)
        # TODO: the out_list part is unessary
        out_list.append(line)


# class Writer(object):
#     """Create an object with a write method that writes to a
#     specific place on the screen, defined at instantiation.
#
#     This is the glue between blessings and progressbar.
#     """
#     def __init__(self, location):
#         """
#         Input: location - tuple of ints (x, y), the position
#                           of the bar in the terminal
#         """
#         self.location = location
#
#     def write(self, string):
#         with term.location(*self.location):
#             print(string)
#
#
# def test(pool, location):
#     """Test with a single bar.
#
#     Input: location - tuple (x, y) defining the position on the
#                       screen of the progress bar
#     """
#     # fd is an object that has a .write() method
#     writer = Writer(location)
#     # pool.apply_async(do_work, (work, results))

def split_input(input_file):
    cmd1 = 'wc -l %s' % input_file
    sub = subprocess.Popen(shlex.split(cmd1), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
    half = int(sub.communicate()[0].split()[0]) / 2 + 1
    cmd2 = '/usr/bin/split -%s %s %s' % (half, input_file, str(input_file) + '_')
    sub2 = subprocess.Popen(shlex.split(cmd2), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
    sub2.communicate()


if __name__ == "__main__":
    manager = Manager()
    term = Terminal()
    file = str(sys.argv[1])
    file_struct = file.split('/')
    # split_input(file)
    # scope = 'ams-2011B-ISS.B620-pass4'
    rse_prefix = '/eos/ams/amsdatadisk/'
    scope = 'protons.B620dev'
    current_line = None
    write_dir = '/afs/cern.ch/user/c/cchao2/rucyio/pass4/result/' + file_struct[-1] + '/'
    num_workers = 64
    try:
        destSE = str(sys.argv[2])
    except:
        destSE = 'tw-eos03'

    results = manager.list()
    work = manager.Queue(num_workers)

    # start for workers
    pool = []
    # pool = Pool()
    # pool = Pool(processes=num_workers)
    # locations = [(0, i) for i in range(0, num_workers)]
    # pool.map(test, (pool,locations))
    # pool.close()
    for i in xrange(num_workers):
        # x_param = (i) * 100
        # with term.location(10, x_param):
        p = Process(target=do_work, args=(work, results))
        p.start()
        pool.append(p)
    # workers = pool.apply_async(do_work, (work, results))
    # produce data
    with open(file) as f:
        iters = itertools.chain(f, (None,) * num_workers)
        for num_and_line in enumerate(iters):
            # num_and_line is a tuple
            # Example:
            # (0, '1383594243.00000001.root\n')
            work.put(num_and_line)

    # for p in pool:
    #    p.join()

    print 'finished'
