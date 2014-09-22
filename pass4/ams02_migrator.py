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
# print os.getcwd()
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
"""
readline from file,
xrdcp to destination
write result in the write_dir
"""
    with open(file, 'rw') as file1:
        for line in file1:
           global current_line
           global count
           current_line = line
           count = count + 1
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/%s root://tw-eos01.grid.sinica.edu.tw/%s' % (line.rstrip(), hash(scope, line))
           cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1343856875.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1343856875.00000001.root'
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1373572204.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1373572204.00000001.root'
           try:
               # sub = subprocess.check_call(shlex.split(cmd), stdout=None, stderr=None)
               sub = subprocess.check_call(shlex.split(cmd))
               # sub = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
               while sub.poll() is None:
                   l = sub.stdout.readline() # This blocks until it receives a newline.
                   print l
               # When the subprocess terminates print unconsumed output and write to finisged_filelist
               print sub.stdout.read()
               write('finished_filelist', line)
           except subprocess.CalledProcessError as e:
               # In the case of duplicate file
               write('exist_filelist', line)

def write(filepath, message):
"""
write message to filepath
"""
    # make sure that filename is just the name of the file
    if '/' in filepath:
        filename = filepath[filepath.rfind('/')+1:]
    else:
        filename = filepath
    path = write_dir + filepath
    mkdir_p(path[:-len(filename)-1])
    with open(path, 'a+') as file2: 
        file2.write(message)

def mkdir_p(path):
"""
same as mkdir -p
"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

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
            signum = getattr(signal,i)
            signal.signal(signum,sighandler)
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


def main():
    try:
        while True:
            read(file)
    except:
        signal_trapper()

if '__main__':
    main()
        
