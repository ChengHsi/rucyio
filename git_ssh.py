import subprocess, sys, shlex, os
 
 target_dir = sys.argv[1]
new_method = sys.argv[2]
 cmd = 'find %s -name .git' %target_dir
 sub = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
 sub = sub.communicate()
old_string = 'https://github.com/'
new_string = 'ssh://git@github.com/'
old_string = 'git://github.com/'
new_string = '$s://git@github.com/', $new_method

 for x in sub[0].split('\n')[:-1]:
     print x
     prev_dir = os.getcwd()
