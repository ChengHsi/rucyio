#!/usr/bin/env python

"""
AMS02 - Paramigrator

parellel version of ams02-migrator 
read from filelist
xrdcp to destination
at the start of each run, the finished_filelist and the existed_filelist should be consistent, not exactly the same, but at least same wc -l
"""

#
# Code goes here.
#
from multiprocessing import Process, Manager
import time
import itertools 
import sys, os, hashlib, subprocess, shlex, signal, datetime, time, errno
import mmap
# print os.getcwd()
file = str(sys.argv[1])
# print os.chdir(file1)
scope = 'ams-2011B-ISS.B620-pass4'
count = 0
current_line = None
write_dir = '/afs/cern.ch/user/c/cchao2/rucyio/pass4/result/'
num_workers = 8 

def hash(scope, line):
    hstr = hashlib.md5('%s:%s' % (scope, line)).hexdigest()
    return '/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/' + '%s/%s/%s' % (hstr[0:2], hstr[2:4], line.rstrip())


def read(file):
    """
    readline from file,
    xrdcp to destination
    """
    with open(file, 'r') as file1:
        for line in file1:
            global current_line
            global count
            current_line = line
            count = count + 1
            xrdcp(line)

def xrdcp(line):
    """
    """
    cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/%s root://tw-eos01.grid.sinica.edu.tw/%s' % (line.rstrip(), hash(scope, line))
    # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1343856875.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1343856875.00000001.root'
    # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1373572204.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1373572204.00000001.root'
    try:
        #TODO: lack a parrelell stdout interface, maybe because i am using check_all instead of Popen? thought it is neccessary for getting the duplicate exception
        # sub = subprocess.check_call(shlex.split(cmd), stdout=None, stderr=None)
        sub = subprocess.check_call(shlex.split(cmd))
        print '\n %s finished. \n' %(line.rstrip())
        # sub = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        # while sub.poll() is None:
        #    l = sub.stdout.readline()  # This blocks until it receives a newline.
        #    print l
        # When the subprocess terminates print unconsumed output and write to finished_filelist
        # print sub.stdout.read()
        write('finished_filelist', line)
    except subprocess.CalledProcessError:
        # In the case of duplicate file
        write('exist_filelist', line)

def write(filepath, message):
    """
    write message to filepath
    """
    # make sure that filename is just the name of the file
    if '/' in filepath:
        filename = filepath[filepath.rfind('/') + 1:]
    else:
        filename = filepath
    path = write_dir + filepath
    mkdir_p(path[:-len(filename) - 1])
    with open(path, 'a+') as file2:
        # somehow file2 has to be already existant for mmap, a fancy way to prevent duplication
        s = mmap.mmap(file2.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find(message) == -1:
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
    message = 'caught signal ' + str(signum) + ' at: ' + timestamp() + '\n' + str(count) + ' ' + str(current_line) + '\n'
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
        if line == None:
            return
        
        # work
        xrdcp(line)
        # TODO: the out_list part is unessary
        out_list.append(line)


if __name__ == "__main__":

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
        iters = itertools.chain(f, (None,)*num_workers)
        for num_and_line in enumerate(iters):
            work.put(num_and_line)

    for p in pool:
        p.join()
    
    # TODO: get rid of this part
    # get the results
    # example:  [(1, "foo"), (10, "bar"), (0, "start")]
    print sorted(results)
