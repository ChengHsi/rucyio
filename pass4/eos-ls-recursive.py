#!/usr/bin/env python

"""
Eos Recusive ls

some function when I need to recursive ls through a Eos directory
"""
import subprocess, shlex, os, sys


def eos_ls_recur(abs_path):
    '''
    this function mimics eos ls -r 
    ''' 
    dir_list = [line.rstrip() for line in open(os.getcwd() + '/hash_dir_name')]
    counter = 0
    # for target_dir in dir_list:
    #   for target_dir2 in dir_list:
          
    for target_dir, target_dir2 in [(x,y) for x in dir_list for y in dir_list]:
        cmd = 'eos ls -a %s%s/%s' %(abs_path, target_dir, target_dir2)
    #import itertools
    #for target_dir in itertools.product(dir_list, repeat=2):
    #    cmd = 'eos ls -a %s%s/%s' %(abs_path, str(target_dir[0]), str(target_dir[1]))
        # print cmd
        # cmd2 = 'eos ls -al /eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/ff/1d/1376007942.00000001.root'
        # sub = subprocess.check_call(shlex.split(cmd), stderr=subprocess.STDOUT) #, stdout=subprocess.PIPE) #, stderr=None)
        try:
            # sub = subprocess.check_call(shlex.split(cmd2), stderr=subprocess.STDOUT, stdout=subprocess.PIPE) #, stderr=None)
            sub = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_tuple = sub.communicate()
            # print str(std_tuple[1])
            # check_all with try except will spit out all the eos ls including errors, so I will stick with Popen
            # and raise my own CalledProcessError
            if str(std_tuple[1]) != '':
                # raise subprocess.CalledProcessError(cmd='args', output='')
                raise subprocess.CalledProcessError(cmd, '') 
            else:
                print abs_path + target_dir + '/' + target_dir2 + ':'
                # print abs_path + str(target_dir[0]) + '/' + str(target_dir[1]) + ':'
                print std_tuple[0].lstrip('.\n..\n')
                if sys.argv[1] = None:
                    f_write = open('tw_eos02_result', 'a')
                    f_write.write(std_tuple[0].lstrip('.\n..\n'))
                else:
                # return std_tuple[0].lstrip('.\n..\n')
                    f_write = open(sys.argv[1], 'a')
                    f_write.write(std_tuple[0].lstrip('.\n..\n'))
                counter += 1
        except subprocess.CalledProcessError:
            pass 
        except KeyboardInterrupt:
            sys.exit()
        except:
            print 'Unknown Error', sys.exc_info()
        if counter == 10:
            sys.exit()
        # break
    # break
    
     
        # if stderr_data == 'None':
        # f_write.write(std_tuple[0])
        # print std_tuple[0]

def eos_ls_recur2():
    '''
    this function mimics eos ls -r
    '''
    dir_list = [line.rstrip() for line in open(os.getcwd() + '/hash_dir_name')]
    # for x, y in map(None, dir_list, dir_list):
    #    print x, y
    # for x, y in [(x,y) for x in dir_list for y in dir_list]:
    #    print x, y
    import itertools
    for x in  itertools.product(dir_list, repeat=2):
        print x[0] + '/' + x[1]

def read_flat_list_and_output_root_lines():
    f_write = open('pass4-filename-eos', 'r+') 
    with open('/root/chchao/eos_result_all', 'r') as lines:
        for line in lines:
            if '.root' in line:
                f_write.write(line)
                print line.rstrip('\n')

if __name__ == '__main__':
    abs_path = '/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/'
    # read_flat_list_and_output_root_lines()
    eos_ls_recur(abs_path)
    # write(abs_path)
