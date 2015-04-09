import subprocess
import shlex
import itertools
result = []
count = 0
check = 'cern-protons-B620dev-pr.pl1.2004000-filelist'
check_against = 'cern-protons-B620dev-other-filelist'
with open(check, 'r') as chk:
    with open(check_against, 'r') as chk_against:
        cmd = 'wc -l %s' % chk.name
        sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
        print sub.communicate()[0].rstrip()
        cmd = 'wc -l %s' % chk_against.name
        sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
        print sub.communicate()[0].rstrip()
        for line in chk:
            for line2 in chk_against:
                count += 1
                if line2.rstrip() == line.rstrip():
                    result.append(line2)
                    break
            chk_against.seek(0)
        print len(result)
        print count
