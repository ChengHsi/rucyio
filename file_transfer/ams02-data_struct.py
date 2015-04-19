"""
ams02-data_struct

This function(script) is used to apply data structure to transfered AMS files,
identified by it's epoch time in its name.
"""
import datetime
import os, sys
from rucio.client.didclient import DIDClient
from rucio.common.exception import DataIdentifierAlreadyExists, Duplicate, RucioException
didCli = DIDClient()

current_dir = os.getcwd()
scope = 'ams-2011B-ISS.B620-pass4'

def default_struct():
    """
    If the scope is clean and the list is sorted.
    """
    with open(current_dir + '/pass4-filelist_all', 'r') as file01:
        # count = 0
        previous_container = ''
        previous_dataset = ''
        attachments = {}
        for line in file01:
            ts_epoch = int(line.split('.')[0])
            container = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d')
            dataset = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d_%H')
            if previous_container != container:
                # print '|', container
                try:
                    didCli.add_did(scope=scope, name=container, type='CONTAINER', statuses=None, meta=None, rules=None, lifetime=None)
                except DataIdentifierAlreadyExists:
                    pass
                previous_container = container
            metadata = didCli.get_metadata(scope, line.rstrip())
            # print metadata
            if previous_dataset != dataset:
                if attachments:
                    # print 'Trying to attach:', attachments.values()
                    try:
                        didCli.attach_dids_to_dids(attachments.values())
                        print 'Attached:', attachments.values()
                        # raw_input("Press Enter to continue...")
                    except Duplicate:
                        pass
                    except RucioException as e:
                        if 'IntegrityError' in str(e):
                            pass
                        else:
                            print e
                    attachments = {}
                # print '|-', dataset
                try:
                    didCli.add_did(scope=scope, name=dataset, type='DATASET', statuses=None, meta=None, rules=None, lifetime=None)
                except DataIdentifierAlreadyExists:
                    pass
                # print '| |-', line.rstrip()
                attachment = {'scope':scope, 'name': dataset, 'rse': 'TW-EOS01_AMS02DATADISK', 'dids': [{'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']}]}
                attachments[dataset] = attachment
                previous_dataset = dataset
            elif previous_dataset == dataset:
                # print '| |-', line.rstrip()
                attachments[dataset]['dids'].append({'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']})
            else:
                raise Exception('Didn\'t expect this!')
    
            # count += 1
            # if count > 10:
            #     break

def single_struct(filelist):
    '''
    Create structure for a list of file.
    ''' 
    previous_container = ''
    previous_dataset = ''
    attachments = {}
    line = None
    for line in filelist:
        ts_epoch = int(line.split('.')[0])
        container = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d')
        dataset = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d_%H')
        if previous_container != container:
            print '|', container
            try:
                didCli.add_did(scope=scope, name=container, type='CONTAINER', statuses=None, meta=None, rules=None, lifetime=None)
            except DataIdentifierAlreadyExists:
                pass
            previous_container = container
        metadata = didCli.get_metadata(scope, line.rstrip())
        print metadata
        if previous_dataset != dataset:
            print '|-', dataset
            try:
                didCli.add_did(scope=scope, name=dataset, type='DATASET', statuses=None, meta=None, rules=None, lifetime=None)
            except DataIdentifierAlreadyExists:
                pass
            print '| |-', line.rstrip()
            if attachments:
                print 'Trying to attach:', attachments.values()
                try:
                    didCli.attach_dids_to_dids(attachments.values())
                except Duplicate:
                    pass
                attachments = {}
            attachment = {'scope':scope, 'name': dataset, 'rse': 'TW-EOS02_AMS02DATADISK', 'dids': [{'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']}]}
            attachments[dataset] = attachment
            previous_dataset = dataset
        elif previous_dataset == dataset:
            print '| |-', line.rstrip()
            attachments[dataset]['dids'].append({'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']})
        else:
            raise Exception('Didn\'t expect this!')
    try:
        didCli.attach_dids_to_dids(attachments.values())
    except Duplicate:
        pass

if __name__ == '__main__':
    default_struct()
    # single_struct(['1325724163.00411408.root'])
