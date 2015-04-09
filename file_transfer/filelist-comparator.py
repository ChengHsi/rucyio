#!/usr/bin/env python

"""
filelist-comparator

This is a modification from eosd, and is used to compare two filelist.
Currently the use case is a full eos find filelist from CERN such as cern-pass6-filelist,
and a filelist from local SE such as tw-eos03-pass6-filelist,
the FilelistComparator diff the two lists and output two diff result in the ./comparator_results/.
"""
import os
import sys
import argparse


def eos_find2dict(filepath):
    '''
    Recieve filelist results from eos find -f --size --checksum and returns JSON-like dictionary of files and its attributes.

    An example of the command to be run on the SE:
    [root@tw-eos02 pass4]# eos find -f --checksum --size /eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/ >> pass4/tw-eos02-pass6-filelist20150303
    Preferably, the naming of the filelist is [SE]-[scope]-filelist-timestamp.
    An example line from eos find -f --size --checksum:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/00/2c/1376848948.00000001.root size=6334587289 checksum=b9816528
    An example of output would be:
    {'1305955357.00733835.root': {'adler32': '00000000', 'name': '1305955357.00733835.root', 'path': '/eos/ams/ams...00733835.root', 'size': '0'}}
    '''
    result_dict = {}
    with open(filepath) as f1:
        import re
        try:
            for line in f1:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                filename = file_spec[1].split('/')[-1:][0]
                result_dict[filename] = {'size': file_spec[3], 'name': filename, 'path': file_spec[1], 'adler32': file_spec[5]}
            return result_dict
        except:
            raise Exception('This function requires the input file to be from eos find -f --size --checksum!')


def file2set(filepath, attr='name'):
    '''
    Return a set from one column(attr) of a file.
    '''
    # raw_list = []
    result = set()
    with open(filepath) as raw:
        for line in raw:
            # raw_list.append(line.rstrip())
            result.add(line.rstrip())
        # result = set(raw_list)
        # print result
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

    For current use:
    {'1305955357.00733835.root': {'adler32': '00000000', 'name': '1305955357.00733835.root',      'path': '/eos/ams/ams...00733835.root', 'size': '0'}}
    The keys such as '1305955357.00733835.root' would be extracted.
    '''
    result = set()
    for key in target_dict.keys():
        result.add(key)
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
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    print 'There are ' + str(len(result)) + ' files from ' + str(ori_name) + ' - ' + str(new_name)
    print 'There are ' + str(len(result2)) + ' files from ' + str(new_name) + ' - ' + str(ori_name)
    write_f = ori_dir + '/comparator_results/missing-from_%s_compare-to_%s_' % (ori_name, new_name) + timestamp
    write_f2 = ori_dir + '/comparator_results/missing-from_%s_compare-to_%s_' % (new_name, ori_name) + timestamp
    # write_f = ori_dir + '/comparator_results/missing-from_' + ori_name + '_compare-to_' + new_name + '_' + timestamp
    # write_f2 = ori_dir + '/comparator_results/missing_from-' + new_name + '-compare_to-' + ori_name + '-' + timestamp
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
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('Filename', metavar='File1', type=str, help='Filename1')
    parser.add_argument('Filename', metavar='File2', type=str, help='Filename1')
    parser.add_argument('-s', '--simple', action='store_true', help='Filelists with only filenames')
    args = parser.parse_args()

    current_dir = os.getcwd()
    ori_name = sys.argv[1]
    ori_path = os.path.abspath(ori_name)
    ori_dir = os.path.dirname(os.path.dirname(ori_path))
    ori_name = sys.argv[1].split('/')[-1]
    new_name = sys.argv[2]
    new_path = os.path.abspath(new_name)
    new_name = sys.argv[2].split('/')[-1]
    result1 = []
    result2 = []
    # try:
    if args.simple:
        print 'Simple compare.'
        result_tuple = sets_diff(ori_set=file2set(ori_path), new_set=file2set(new_path))
    else:
        ori_dict = eos_find2dict(ori_path)
        new_dict = eos_find2dict(new_path)
        result_tuple = sets_diff(ori_set=dict2set(ori_dict), new_set=dict2set(new_dict))
        for file in result_tuple[0]:
            result1.append('path=%s size=%s checksum=%s' % (ori_dict[file]['path'], ori_dict[file]['size'], ori_dict[file]['adler32']))
        for file in result_tuple[1]:
            result2.append('path=%s size=%s checksum=%s' % (ori_dict[file]['path'], ori_dict[file]['size'], ori_dict[file]['adler32']))
        result_tuple = (result1, result2)

    # except IndexError:
    #     new_name = 'SE'
    #     result_tuple = sets_diff(ori_set=file2set(ori_path), new_set=set_intersect(get_filepath_list(['tw-eos01', 'tw-eos02', 'tw-eos03'])))
    write_result(ori_name, new_name, result_tuple)
