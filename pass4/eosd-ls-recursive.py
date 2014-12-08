#!/usr/bin/env python

"""
Eosd Recusive ls

some function when I need to recursive ls through a Eos directory
with eosd enabled
"""
import subprocess, shlex, os, sys

def read_raw_ls_r_and_output_lines_of_file():
    with open('/root/chchao/rucyio/pass4/tw-eos01-ls-result_01', 'w+') as f_write:
        with open('/root/chchao/rucyio/pass4/tw-eos01-ls-result_00', 'r') as lines:
            for line in lines:
                if '-rw-r--r--' in line:
                    f_write.write(line)
                    print line.rstrip('\n')
def merge_2files_by_common_id(filepath1, filepath2):
    '''
    Merge results from eos ls -l and eos find by common identifier filename.
    
    An example line from eos ls -l:
    -rw-rw-r-- 1 twgridpil twgridpil 6334587289 Nov 14 21:04 1376848948.00000001.root
    An example line from eos find -f --checksum:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/02/05/1370420623.0000000
    1.root checksum=cd61aeb0
    '''
    with open(filepath1) as f1, open(filepath2 as f2):
        raw_list = []
        if 'result_01' in filepath1 and 'result_adler' in filepath2:
	    eos_ls = f1
	    eos_find = f2
	elif 'result_adler' in filepath1 and 'result_01' in filepath2:
	    eos_ls = f1
	    eos_find = f2
	else:
	    raise Exception('this should not happen!')
            
        for line in eos_ls: 
            try:
                file_spec = line.rstrip().split()
                file_spec_dict = {'size':int(file_spec[4]), 'name':file_spec[8]}
                if file_spec_dict['size'] > 0:
                    # result_list.append({file_spec_dict['name']:file_spec_dict})
                    result_list.append({file_spec_dict})
            
            except ValueError:
                print 'Value error on', line
		raise ValueError

	for line in eos_find:
	    try:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                # file_spec_dict['name']
                # file_spec_dict['checksum']
                return file_spec
            except:
                raise Exception('Not implemented')

def raw2set(result_list):
    for items in result_list:
        elif 'result_00' in filepath:
            '''result_00 are lines with files and directory from ll -R'''
            # for line in raw:
            #    raw_list.append(line)
            raise Exception('Not implemented!')
        elif 'result__adler' in filepath:
            # for line in 
            pass
        else:
            for line in raw:
                raw_list.append(line.rstrip())
        result = set(raw_list)
        print 'There are ' + str(len(result)) +' files in ' + filepath
        return result

def add_checksum(filepath):
    '''
    Parse result from eos find, which are stored as *result_adler.
    a example line would be:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/02/bf/1378509932.0000000\
    1.root checksum=efc29e3d
    '''
    import re
    with open(filepath) as chksum_f:
        if 'result_adler' in filepath:
            for line in chksum_f:
                try:
    

def set_intersect(filepath_list):
    result_set = set()
    for file in filepath_list:
        result_set = result_set | raw2set(file)
    return result_set

def get_filepath_list(se_list):
    result = []
    for se in se_list:
        path_01 = pass4_dir + '/' + se + '-ls-result_01'
        result.append(path_01)
    return result

def sets_diff(ori_set, new_set):
    result  = ori_set - new_set
    print 'There are ' + str(len(result)) +' file differntials'
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(pass4_dir + '/missing_on_se_' + timestamp, 'w+') as f_write:
        for file in result:
            f_write.write(file)
            f_write.write('\n')


if __name__ == '__main__':
    result_list = []
    current_dir = os.getcwd()
    if 'pass4' not in current_dir:
        pass4_dir = current_dir + '/pass4'
    else:
        pass4_dir = current_dir
    ori_path = pass4_dir + '/pass4-filelist_all'
    ## read_raw_ls_r_and_output_lines_of_file()
    # ori_set = raw2set(ori_path)
    # new_set = set_intersect(get_filepath_list(['tw-eos01', 'tw-eos02', 'tw-eos03']))
    # sets_diff(ori_set, new_set)
    print add_checksum(pass4_dir+'/'+'tw-eos03-ls-result_adler')
