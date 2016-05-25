import sys
import csv
file = sys.argv[1]
shownrow = 3
with open(file, 'rb') as file:
    arkreader = csv.DictReader(file)
    count = 0
    for line in arkreader:
        if line['ARK ID']!='#N/A' and line['ARK ID'] is not '':
            # print line['obj_name'], line['Gri_size(bytes)'], line['Gri_md5'], line['s3_md5'], line['ARK ID']
            return_dict = dict((k, line[k]) for k in ('obj_name', 'Gri_size(bytes)', 'ftp_md5 check', 'ARK ID'))
            return_dict['name'] = return_dict.pop('obj_name')
            return_dict['size'] = return_dict.pop('Gri_size(bytes)')
            return_dict['md5'] = return_dict.pop('ftp_md5 check').split('-')[0]
            return_dict['path'] = return_dict['ARK ID'][return_dict['ARK ID'].index('ark:/'):]
            return_dict.pop('ARK ID')
            with open('arkid_filelist', 'a') as f_write:
                f_write.write(str(return_dict))
                f_write.write('\n')
            print return_dict
        #    count +=1
        # if count > shownrow:
        #     break
