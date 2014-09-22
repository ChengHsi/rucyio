#
## Code goes here.
#

import sys, os, hashlib, subprocess, shlex, signal
# print os.getcwd()
file = str(sys.argv[1])
# print os.chdir(file1)
scope = 'ams-2011B-ISS.B620-pass4'
count = 0
current_line = None
def hash(scope, line):
    hstr = hashlib.md5('%s:%s' % (scope, line)).hexdigest()
    return '/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/' + '%s/%s/%s' % (hstr[0:2], hstr[2:4], line)

def read(file):
    with open(file, 'r') as file1:
        for line in file1:
           global current_line
           global count
           current_line = line
           count = count + 1
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/%s root://tw-eos01.grid.sinica.edu.tw/%s' % (line.rstrip(), hash(scope, line))
           cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1343856875.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1343856875.00000001.root'
           # cmd = 'xrdcp root://eosams.cern.ch//eos/ams/Data/AMS02/2011B/ISS.B620/pass4/1373572204.00000001.root root://tw-eos01.grid.sinica.edu.tw//eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/6f/ed/1373572204.00000001.root'
           # print hash(scope, line)

           # sub = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
           except subprocess.CalledProcessError as e:
               print 'File exist: write to /afs/cern.ch/user/c/cchao2/rucyio/pass4/exist_file'
               with open('/afs/cern.ch/user/c/cchao2/rucyio/pass4/exist_file', 'wr') as file2:
                    file2.write(line)
           # break


def sighandler():
    with open('/afs/cern.ch/user/c/cchao2/rucyio/pass4/just_in_case', 'wr') as file3:
        file3.write(str(count) + ' ' + str(current_line))

def main():
    try:
        while True:
            read(file)
    except KeyboardInterrupt:
        print count
        sighandler()
    for i in [x for x in dir(signal) if x.startswith("SIG")]:
        try:
            signum = getattr(signal,i)
            signal.signal(signum,sighandler())
        except RuntimeError,m:
            print "Skipping %s"%i



