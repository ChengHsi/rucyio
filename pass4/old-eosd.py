#!/usr/bin/env python

"""
Eosd Utilities

Some function when I need to recursive ls through a Eos directory
with eosd enabled
"""
import subprocess, shlex, os, sys

def file_only_eosd_ls_r():
    '''
    Filter lines of file from ls -R result when using eosd service.

    Raw result with subdirectories is assummed to be named *result_00,
    and se-ls-result_01 would be written.
    '''
    with open('/root/chchao/rucyio/pass4/tw-eos01-ls-result_01', 'w+') as f_write:
        with open('/root/chchao/rucyio/pass4/tw-eos01-ls-result_00', 'r') as lines:
            for line in lines:
                if '-rw-r--r--' in line:
                    f_write.write(line)
                    print line.rstrip('\n')


def join_by_common(filepath1, filepath2):
    '''
    Merge results from eos ls -l and eos find by common identifier filename.

    An example line from eos ls -l:
    -rw-rw-r-- 1 twgridpil twgridpil 6334587289 Nov 14 21:04 1376848948.00000001.root
    An example line from eos find -f --checksum:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/02/05/1370420623.0000000
    1.root checksum=cd61aeb0
    '''
    result_dict = {}
    with open(filepath1) as f1:
        with open(filepath2) as f2:
            if ('result_01' in filepath1 and 'result_adler' in filepath2):
	            eos_ls = f1
	            eos_find = f2
            elif ('result_adler' in filepath1) and ('result_01' in filepath2):
	            eos_ls = f2
	            eos_find = f1
            else:
	            raise Exception('this should not happen!')
            for line in eos_ls:
                try:
                    file_spec = line.rstrip().split()
                    file_spec_dict = {'size':int(file_spec[4]), 'name':file_spec[8]}
                    if file_spec_dict['size'] > 0:
                        result_dict[file_spec_dict['name']] = file_spec_dict
                    else:
                        print file_spec_dict['name']
                except ValueError:
                    print 'Value error on', line
                    raise ValueError

            import re
            import pdb; pdb.set_trace()
            for line in eos_find:
                # try:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                filename = file_spec[1].split('/')[-1:][0]
                result_dict[filename]['path'] = file_spec[1]
                result_dict[filename]['adler32'] = file_spec[3]
                # except :
                #     raise Exception('Unexpected Error', sys.exc_info()[0])
            return result_dict

def file2set(filepath, attr='name'):
    '''
    Return a set from one column(attr) of a file.
    '''
    with open(filepath) as raw:
        raw_list = []
        if 'result_01' in filepath:
            '''result_01 are rawlists of files directly from a eosd ll -R'''
            for line in raw:
                try:
                    file_spec = line.rstrip().split()
                    file_spec_dict = {'size':int(file_spec[4]), 'name':file_spec[8]}
                    if file_spec_dict['size'] > 0:
                        raw_list.append(file_spec_dict['name'])
                except ValueError:
                    print line
        elif 'result_00' in filepath:
            '''result_00 are lines with files and directory from ll -R'''
            # for line in raw:
            #    raw_list.append(line)
            raise Expection('Not implemented!')
        else:
            for line in raw:
                raw_list.append(line.rstrip())
        result = set(raw_list)
        print 'There are ' + str(len(result)) +' files in ' + filepath
        return result

def dict_list2set(result_list, attr='name'):
    '''
    Return a set from one attribute of a list of dictionaries.
    '''
    for items in result_list:
        result = set()
        result.add(items[attr])
        print 'There are ' + str(len(result)) +' files in the list'
        return result

# def set_intersect(filepath_list):
#     result_set = set()
#     for file in filepath_list:
#         result_set = result_set | file2set(file)
#     return result_set

def get_filepath_list(se_list):
    result = []
    for se in se_list:
        path_01 = pass4_dir + '/' + se + '-ls-result_01'
        result.append(path_01)
    return result

def sets_diff(ori_set, new_set):
    result  = ori_set - new_set
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print 'There are ' + str(len(result)) +' file differntials'
    print wrte to ass4_dir + '/missing_on_se_' + timestamp
    with open(pass4_dir + '/missing_on_se_' + timestamp, 'w+') as f_write:
        for file in result:
            f_write.write(file)
            f_write.write('\n')



if __name__ == '__main__':
    current_dir = os.getcwd()
    if 'pass4' not in current_dir:
        pass4_dir = current_dir + '/pass4'
    else:
        pass4_dir = current_dir
    ori_path = pass4_dir + '/pass4-filelist_all'
    ## file_only_eosd_ls_r()
    # sets_diff(ori_set=file2set(ori_path), new_set=set_intersect(get_filepath_list(['tw-eos01', 'tw-eos02', 'tw-eos03'])))
    join_by_common(pass4_dir+'/'+'tw-eos02-ls-result_adler', pass4_dir+'/'+'tw-eos02-ls-result_01')
