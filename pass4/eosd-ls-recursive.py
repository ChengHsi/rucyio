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

def raw2set(filepath):
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
    current_dir = os.getcwd()
    if 'pass4' not in current_dir:
        pass4_dir = current_dir + '/pass4'
    else:
        pass4_dir = current_dir
    ori_path = pass4_dir + '/pass4-filelist_all'
    # read_raw_ls_r_and_output_lines_of_file()
    ori_set = raw2set(ori_path)
    new_set = set_intersect(get_filepath_list(['tw-eos01', 'tw-eos02', 'tw-eos03']))
    sets_diff(ori_set, new_set)
