import subprocess
sub = subprocess.Popen(["find", "/", "-name", ".git"], stdout=subprocess.PIPE)
sub = sub.communicate()
old_string = 'https://github.com/'
new_string = 'ssh://git@github.com/'
for x in sub[0].split('\n')[:-1]:
    x = x + '/config'
    s = open(x).read()
    if old_string in s:
        s = s.replace(old_string, new_string)
        f = open(x, 'w')
        f.write(s)
        f.flush()
        f.close()
