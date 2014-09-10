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

def filelist_diff(file1, file2):
    list1 = [line.rstrip() for line in open(file1)]
    list2 = [line.rstrip() for line in open(file2)]
    #if list1 > list2:
    missing_list = list(set(list1)-set(list2))
    why_list = list(set(list2)-set(list1))
    f_write1 = open('pass4-filediff-missingfromruciodb01', 'w+')
    f_write2 = open('pass4-filediff-inruciodb01butnotonfelixslist', 'w+')
    for name in missing_list:
        f_write1.write(name + '\n')
    for name in why_list:
        f_write2.write(name + '\n')
#read_flat_list_and_output_root_lines()
filelist_diff('/asgc_ui_home/chchao/git/rucyio/pass4/pass4-filelist_all', '/asgc_ui_home/chchao/git/rucyio/pass4/pass4-filelist_rucio-db01')
