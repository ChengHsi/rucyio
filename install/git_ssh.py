import subprocess, os
subprocess.call(["git", "config", "user.name", "Cheng-Hsi Chao"])
subprocess.call(["git", "config", "user.email", "curiojustus@gmail.com"])
sub = subprocess.Popen(["find", os.environ['HOME'], "-name", ".git"], stdout=subprocess.PIPE)
sub = sub.communicate()
old_string = 'https://github.com/'
new_string = 'ssh://git@github.com/'
for x in sub[0].split('\n')[:-1]:
    print x
    prev_dir = os.getcwd()
    os.chdir(x)
    #pwd = subprocess.Popen('pwd', stdout=subprocess.PIPE)
    test = subprocess.Popen(["git", "remote", "show", "origin"], stdout=subprocess.PIPE)
    if 'ChengHsi' in test.communicate()[0]:
        x = x + '/config'
        s = open(x).read()
        if old_string in s:
            print 'replacing',old_string, 'in', x, 'with', new_string
            s = s.replace(old_string, new_string)
            f = open(x, 'w')
            f.write(s)
            f.flush()
            f.close()
    os.chdir(prev_dir)
