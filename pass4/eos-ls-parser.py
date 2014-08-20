import subprocess, shlex

def flat_list_from_eos_ls():
    f_write = open('eos_result_all', 'w+')
    dir_list = [line.rstrip() for line in open('/root/chchao/hash_dir_name')]
    for target_dir in dir_list:
        for target_dir2 in dir_list:
            cmd = 'eos ls -a eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4//%s/%s' %(target_dir, target_dir2)
            sub = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=None)
            std_tuple = sub.communicate()
            #if stderr_data == 'None':
            f_write.write(std_tuple[0])
            print std_tuple[0]

def read_flat_list_and_output_root_lines():
    f_write = open('pass4-filename-eos', 'w+') 
    with open('/root/chchao/eos_result_all', 'r') as lines:
        for line in lines:
            if '.root' in line:
                f_write.write(line)
                print line.rstrip('\n')
read_flat_list_and_output_root_lines()
