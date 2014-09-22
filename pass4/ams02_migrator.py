#!/usr/bin/env python

"""
read and xrdcp

read from filelist
xrdcp to destination
"""

#
## Code goes here.
#

import sys, os, hashlib, subprocess, shlex, signal, datetime, time, errno
print os.getcwd()
file = str(sys.argv[1])
# print os.chdir(file1)
scope = 'ams-2011B-ISS.B620-pass4'
count = 0
current_line = None
write_dir = '/afs/cern.ch/user/c/cchao2/rucyio/pass4/result/'

def hash(scope, line):
    hstr = hashlib.md5('%s:%s' % (scope, line)).hexdigest()
    return '/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/' + '%s/%s/%s' % (hstr[0:2], hstr[2:4], line)

def read(file):
    with open(file, 'rw') as file1:
        for line in file1:
           global current_line
           global count
           current_line = line
           count = count + 1
           cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/%s root://tw-eos01.grid.sinica.edu.tw/%s' % (line.rstrip(), hash(scope, line))
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1343856875.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1343856875.00000001.root'
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1373572204.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1373572204.00000001.root'
           try:
               # sub = subprocess.check_call(shlex.split(cmd), stdout=None, stderr=None)
               sub = subprocess.check_call(shlex.split(cmd))
               # sub = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
               while sub.poll() is None:
                   l = sub.stdout.readline() # This blocks until it receives a newline.
                   print l
               # When the subprocess terminates there might be unconsumed output 
               # that still needs to be processed.
               print sub.stdout.read()
               write('finished_filelist', line)
           except subprocess.CalledProcessError as e:
               write('exist_filelist', line)

def write(filename, line):
    path = str(timestamp()[:10]) + '/' + filename
    mkdir_p(path[:-len(filename)-1])
    with open(path, 'a+') as file2: 
        file2.write(line)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def sighandler(signum, frame):
    with open(str(timestamp()[:10]) + '/sighandler_result', 'a+') as file3:
        file3.write('caught signal ' + str(signum) + ' at: ' + timestamp() + '\n')
        file3.write(str(count) + ' ' + str(current_line))

def timestamp():
    standard_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    return standard_time

def main():
    try:
        while True:
            read(file)
    except:
        for i in [x for x in dir(signal) if x.startswith("SIG")]:
            try:
                signum = getattr(signal,i)
                # print signum, i, signal
                signal.signal(signum,sighandler)
            except RuntimeError,m:
                # print "Skipping %s"%i
                pass
            except ValueError:
                pass 


if '__main__':
    main()
        
