"""
ams02-data_struct

This function(script) is used to apply data structure to transfered AMS files,
identified by it's epoch time in its name.
"""
import datetime
import os
# from rucio.client.didclient import DIDClient
# didCli = DIDClient()

current_dir = os.getcwd()
scope = 'ams-2011B-ISS.B620-pass4'

with open(current_dir + '/pass4-filelist_all', 'r') as file01:
    count = 0
    previous_container = ''
    previous_dataset = ''
    attachments = {}
    for line in file01:
        ts_epoch = int(line.split('.')[0])
        container = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d')
        dataset = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d_%H')
        if previous_container != container:
            # print 'Adding container:', container
            print '|', container
            # didCli.add_did(scope=scope, name=container, type='CONTAINER', statuses=None, meta=None, rules=None, lifetime=None)
            previous_container = container
        if previous_dataset != dataset:
            # print 'Adding dataset:', dataset
            print '|-', dataset
            # didCli.add_did(scope=scope, name=dataset, type='DATASET', statuses=None, meta=None, rules=None, lifetime=None)
            print '| |-', line.rstrip()
            attachment = {'scope':scope, 'name': dataset, 'dids': [{'scope':scope, 'name':line}]}
            attachments[dataset] = attachment
            previous_dataset = dataset
        elif previous_dataset == dataset:
            print '| |-', line.rstrip()
            attachments[dataset]['dids'].append({'scope':scope, 'name':line})
        else:
            raise Exception('Didn\'t expect this!')

        count += 1
        if count > 10:
            break
    # didCli.attach_dids_to_dids(attachments.values())

