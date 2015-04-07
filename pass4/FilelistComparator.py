#!/usr/bin/env python

"""
FileListCompartor

This is a modification of the eosd, and is used to compare two filelist.
"""
import os
import sys
import argparse


def eos_find2dict(filepath1):
    '''
    Recieve results from eos find -f --size --checksum and returns JSON-like dictionary of files and its attributes.
    An example of the command to be run on SE:
    [root@tw-eos02 pass4]# eos find -f --checksum --size /eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/ >> tw-eos02-ls-result_cs
    An example line from eos find -f --size --checksum:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/00/2c/1376848948.00000001.root size=6334587289 checksum=b9816528
    An example of output would be:
    {'1305955357.00733835.root': {'adler32': '00000000', 'name': '1305955357.00733835.root', 'path': '/eos/ams/ams...00733835.root', 'size': '0'}}
    '''
    result_dict = {}
    with open(filepath1) as f1:
        import re
        if 'result_cs' in filepath1:
            for line in f1:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                filename = file_spec[1].split('/')[-1:][0]
                result_dict[filename] = {'size': file_spec[3], 'name': filename, 'path': file_spec[1], 'adler32': file_spec[5]}
            return result_dict
        else:
            raise Exception('this function currently requires *result_cs files a inout!')
        if 'cern-protons-B620dev-all-filelist_cs' in filepath1:
            for line in f1:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                filename = file_spec[1].split('/')[-1:][0]
                result_dict[filename] = {'size': file_spec[3], 'name': filename, 'path': file_spec[1], 'adler32': file_spec[5]}
            return result_dict
        else:
            raise Exception('this function currently requires *result_cs files a inout!')


def file2set(filepath, attr='name'):
    '''
    Return a set from one column(attr) of a file.
    '''
    raw_list = []
    with open(filepath) as raw:
        for line in raw:
            raw_list.append(line.rstrip())
        result = set(raw_list)
        print 'There are ' + str(len(result)) + ' files in ' + filepath
        return result


def dict_list2set(result_list, attr='name'):
    '''
    Return a set from one attribute of a list of dictionaries.
    '''
    result = set()
    for items in result_list:
        result.add(items[attr])
    return result


def dict2set(target_dict):
    '''
    Return a set from keys of dictionaries.
    '''
    result = set()
    for key in target_dict.keys():
        result.add(key)
    print 'There are ' + str(len(result)) + ' files in the set'
    return result


def set_intersect(filepath_list):
    result_set = set()
    for file in filepath_list:
        result_set = result_set | dict2set(eos_find2dict(file))
    return result_set


def get_filepath_list(se_list):
    '''
    From a list of SEs names return the list of its filepath.
    '''
    result = []
    for se in se_list:
        path_01 = ori_dir + '/' + se + '-ls-result_cs'
        result.append(path_01)
    return result


def sets_diff(ori_set, new_set):
    print 'There are ' + str(len(ori_set)) + ' files in orignal set'
    print 'There are ' + str(len(new_set)) + ' files in new set'
    result = ori_set - new_set
    result2 = new_set - ori_set
    return (result, result2)


def write_result(ori_name, new_name, result_tuple):
    result, result2 = result_tuple
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H%M')
    print 'There are ' + str(len(result)) + ' files from ' + str(ori_name) + ' - ' + str(new_name)
    print 'There are ' + str(len(result2)) + ' files from ' + str(new_name) + ' - ' + str(ori_name)
    write_f = ori_dir + '/MISSING_' + timestamp + '_' + ori_name + '_minus_' + new_name
    write_f2 = ori_dir + '/MISSING_' + timestamp + '_' + new_name + '_minus_' + ori_name
    print 'Write to:', write_f
    with open(write_f, 'w+') as f_write:
        for file in result:
            f_write.write(file)
            f_write.write('\n')
    print 'Write to:', write_f2
    with open(write_f2, 'w+') as f_write:
        for file in result2:
            f_write.write(file)
            f_write.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True)
    parser.add_argument('Filename', metavar='File1', type=str, help='Filename1')
    parser.add_argument('Filename', metavar='File2', type=str, help='Filename1')
    args = parser.parse_args(description='')
    # subparsers = oparser.add_subparsers()
    current_dir = os.getcwd()
    try:
        import pdb; pdb.set_trace()
        ori_name = sys.argv[1]
        ori_path = os.path.abspath(ori_name)
        ori_dir = os.path.dirname(ori_path)
        ori_name = sys.argv[1].split('/')[-1]
    except IndexError:
        ori_name = 'pass4-filelist_all'
    try:
        new_name = sys.argv[2]
        new_path = os.path.abspath(new_name)
        new_name = sys.argv[2].split('/')[-1]
        result_tuple = sets_diff(ori_set=file2set(ori_path), new_set=file2set(new_path))
    except IndexError:
        new_name = 'SE'
        result_tuple = sets_diff(ori_set=file2set(ori_path), new_set=set_intersect(get_filepath_list(['tw-eos01', 'tw-eos02', 'tw-eos03'])))
    write_result(ori_name, new_name, result_tuple)
