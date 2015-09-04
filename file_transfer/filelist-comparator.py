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
import json

def eos_find2dict(filepath):
    '''
    Recieve filelist results from eos find -f --size --checksum and returns JSON-like dictionary of files and its attributes.

    An example of the command to be run on the SE:
    [root@tw-eos02 pass4]# eos find -f --checksum --size /eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/ >> pass4/tw-eos02-pass6-filelist20150303
    Preferably, the naming of the filelist is [SE]-[scope]-filelist-timestamp.
    An example line from eos find -f --size --checksum:
    path=/eos/ams/amsdatadisk/ams-2011B-ISS/B620-pass4/00/2c/1376848948.00000001.root size=6334587289 checksum=b9816528
    An example of output would be:
    {'1305955357.00733835.root': {'adler32': '00000000', 'name': '1305955357.00733835.root','size': '0'}}
    '''
    result_dict = {}
    with open(filepath) as f1:
        import re
        try:
            for line in f1:
                file_spec = line.rstrip()
                file_spec = re.split('=|\s', file_spec)
                filename = file_spec[1].split('/')[-1:][0]
                # result_dict[filename] = {'name': filename, 'size': file_spec[3], 'adler32': file_spec[5]}
                result_dict[filename] = {'size': file_spec[3], 'name': filename, 'path': file_spec[1], 'adler32': file_spec[5]}
            return result_dict
        except:
            raise Exception('This function requires the input file to be from eos find -f --size --checksum!')


def result2dict(filepath):
    '''
    Recieve results and returns JSON-like dictionary of files and its attributes.

    An example line:
    name=1376848948.00000001.root size=6334587289 checksum=b9816528
    An example of output would be:
    {'1305955357.00733835.root': {'adler32': '00000000', 'name': '1305955357.00733835.root', 'size': '0'}}
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
                # result_dict[filename] = {'name': filename, 'size': file_spec[3], 'adler32': file_spec[5]}
            return result_dict
        except:
            raise Exception('This function requires the input file to be from eos find -f --size --checksum!')


def file2set(filepath, attr='name'):
    '''
    Return a set from one column(attr) of a file.
    '''
    result = set()
    with open(filepath) as raw:
        for line in raw:
            # raw_list.append(line.rstrip())
            result.add(line.rstrip())
        # result = set(raw_list)
        # print result
    print 'There are ' + str(len(result)) + ' files in ' + filepath
    return result


def dictkey2set(target_dict):
    '''
    Return a set from keys of dictionaries.

    For current use:
    {'1305955357.00733835.root': {'name': '1305955357.00733835.root', 'size': '0', 'adler32': '00000000', }}
    The keys such as '1305955357.00733835.root' would be extracted.
    '''
    result = set()
    for key in target_dict.keys():
        result.add(key)
    return result


def dict2set(target_dict, include_path=False):
    '''
    Return a set of the set of values in the target dictionary.

    For current use:
    {'1305955357.00733835.root': {'name': '1305955357.00733835.root', 'size': '0', 'adler32': '00000000 }}
    a set like set(('1305955357.00733835.root', '0', '00000000'), .....) would be returned
    '''
    if include_path:
        return set((i['name'], i['size'], i['adler32'], i['path']) for i in target_dict.values())
    else:
        return set((i['name'], i['size'], i['adler32']) for i in target_dict.values())


def set2dict(target_set):
    '''
    Return a list of dict from the set of values in the target set.

    For current use:
    {'1305955357.00733835.root': {'name': '1305955357.00733835.root', 'size': '0', 'adler32': '00000000', }}
    a set like set(('1305955357.00733835.root', '0', '00000000'), .....) would be returned
    '''
    # return {i[0]: {'name': i[0], 'size': i[1], 'adler32': i[2]} for i in target_set}
    return dict((i[0], {'name': i[0], 'size': i[1], 'adler32': i[2]}) for i in target_set)


def set_intersect(set1, set2):
    return set1 & set2


def sets_diff(ori_set, new_set):
    print 'There are ' + str(len(ori_set)) + ' files in orignal set'
    print 'There are ' + str(len(new_set)) + ' files in new set'
    # print ori_set
    # print new_set
    result = ori_set - new_set
    result2 = new_set - ori_set
    # print result, result2
    return (result, result2)


def write_result(ori_name, new_name, result_tuple, duplicate_set=None, corrupted_set=None):
    result, result2 = result_tuple
    ori_name, new_name = filename_trim(ori_name), filename_trim(new_name)
    import datetime
    timestamp = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    print 'There are ' + str(len(result)) + ' files from ' + str(ori_name) + ' - ' + str(new_name)
    print 'There are ' + str(len(result2)) + ' files from ' + str(new_name) + ' - ' + str(ori_name)
    if duplicate_set:
        print 'There are %d duplicate files from %s & %s' % (len(duplicate_set), str(ori_name), str(new_name))
    if duplicate_set:
            print 'Seems like %d of files corrupted.' % (len(corrupted_set))
    write_f = ori_dir + '/comparator_results/missing-from_%s_compare-to_%s_' % (ori_name, new_name) + timestamp
    write_f2 = ori_dir + '/comparator_results/missing-from_%s_compare-to_%s_' % (new_name, ori_name) + timestamp
    write_f3 = ori_dir + '/comparator_results/duplicate-from_%s_compare-to_%s_' % (new_name, ori_name) + timestamp
    write_f4 = ori_dir + '/comparator_results/corrupted-from_%s_compare-to_%s_' % (new_name, ori_name) + timestamp
    write_result2(write_f, parse_set(result), ori_dict)
    write_result2(write_f2, parse_set(result2), new_dict)
    write_result2(write_f3, duplicate_set)
    write_result2(write_f4, corrupted_set)


def write_result2(out_file, result, reference_dict=None):
    if result:
        print 'Write to:', out_file
        with open(out_file, 'w+') as f_write:
            for line in result:
                if reference_dict:
                    import json
                    to_write = json.dumps(reference_dict[line.replace('=', ' ').split()[1]]).rstrip('}').lstrip('{').replace('\"', '').replace(': ', '=').replace(',', '').replace('adler32', 'checksum')
                    f_write.write(to_write)
                    f_write.write('\n')
                # elif 'duplicate  in 'out_file:
                else:
                    f_write.write(line)
                    f_write.write('\n')


def filename_trim(filename):
    return filename[:-8]


def parse_set(result):
    return ['name=%s size=%s checksum=%s' % (file[0], file[1], file[2]) for file in result]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('Filename', metavar='File1', type=str, help='Filename1')
    parser.add_argument('Filename', metavar='File2', type=str, help='Filename1')
    parser.add_argument('-vs', '--vsimple', action='store_true', help='Filelists with only filenames')
    parser.add_argument('-s', '--simple', action='store_true', help='Compare only filenames from Filelists')
    parser.add_argument('-d', '--check-duplicate', action='store_true', help='Also check for duplicates between filelists')
    parser.add_argument('-c', '--check-cern', action='store_true', help='Compare local SE filelist with CERNs')
    args = parser.parse_args()
    current_dir = os.getcwd()
    ori_name = sys.argv[1]
    ori_path = os.path.abspath(ori_name)
    ori_dir = os.path.dirname(os.path.dirname(ori_path))
    ori_name = sys.argv[1].split('/')[-1]
    new_name = sys.argv[2]
    new_path = os.path.abspath(new_name)
    new_name = sys.argv[2].split('/')[-1]
    global ori_dict
    global new_dict
    if args.vsimple:
        print 'Very simple compare.'
        result_tuple = sets_diff(ori_set=file2set(ori_path), new_set=file2set(new_path))
    elif args.simple:
        print 'Simple compare.'
        ori_dict = eos_find2dict(ori_path)
        new_dict = eos_find2dict(new_path)
        result_tuple = sets_diff(ori_set=dictkey2set(ori_path), new_set=dictkey2set(new_path))
    else:
        ori_dict = eos_find2dict(ori_path)
        new_dict = eos_find2dict(new_path)
        result_tuple = sets_diff(ori_set=dict2set(ori_dict), new_set=dict2set(new_dict))
        duplicate_path_set = set()
        duplicate_path_list = []
        if args.check_duplicate:
            # import pdb; pdb.set_trace()
            duplicate_set = dict2set(ori_dict) & dict2set(new_dict)
            for i in duplicate_set:
                # duplicate_path_set.add(ori_dict[i[0]]['path'])
                duplicate_path_list.append(json.dumps(ori_dict[i[0]]).rstrip('}').lstrip('{').replace('=', ' ').replace('\"', '').replace(': ', '=').replace(', ', ' ').replace('adler32', 'checksum'))
        corrupted_set = dictkey2set(set2dict(result_tuple[0])) & dictkey2set(set2dict(result_tuple[1]))
        corrupted_path_set = set()
        if corrupted_set:
            for i in list(corrupted_set):
                corrupted_path_set.add(ori_dict[i]['path'])
    # write_result(ori_name, new_name, result_tuple, duplicate_path_set, corrupted_path_set)
    write_result(ori_name, new_name, result_tuple, duplicate_path_list, corrupted_path_set)
