"""
ams02-data_struct

This function(script) is used to apply data structure to transfered AMS files,
identified by it's epoch time in its name.
"""
import datetime
import argparse
import os, sys
from rucio.client.didclient import DIDClient
from rucio.common.exception import DataIdentifierAlreadyExists, Duplicate, RucioException

def default_struct(filelist, scope):
    """
    If the scope is clean and the list is sorted.
    """
    with open(filelist, 'r') as file01:
        previous_container = ''
        previous_dataset = ''
        attachments = {}
        for line in file01:
            did = line.replace('=', ' ').split()[1].split('/')[-1]
            ts_epoch = int(did.split('.')[0])
            container = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d')
            dataset = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d_%H')
            if previous_container != container:
                # print '|', container
                try:
                    didCli.add_did(scope=args.scope, name=container, type='CONTAINER', statuses=None, meta=None, rules=None, lifetime=None)
                except DataIdentifierAlreadyExists:
                    pass
                previous_container = container
            metadata = didCli.get_metadata(scope, did.rstrip())
            print metadata
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

                container_attachment = [{'scope':scope, 'name': container, 'dids': [{'scope':scope, 'name':dataset}]}]
                try:
                    didCli.attach_dids_to_dids(container_attachment)
                    print 'Attached Dataset to Container:', container_attachment
                except RucioException as e:
                    if 'IntegrityError' in str(e):
                        pass
                    else:
                        print e
                # print '| |-', did.rstrip()
                attachment = {'scope':scope, 'name': dataset, 'rse': 'TW-EOS01_AMS02DATADISK', 'dids': [{'scope':scope, 'name':did.rstrip(), 'bytes':metadata['bytes']}]}
                attachments[dataset] = attachment
                previous_dataset = dataset
            elif previous_dataset == dataset:
                # print '| |-', did.rstrip()
                attachments[dataset]['dids'].append({'scope':scope, 'name':did.rstrip(), 'bytes':metadata['bytes']})
            else:
                raise Exception('Didn\'t expect this!')


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
        # print metadata
        if previous_dataset != dataset:
            print '|-', dataset
            try:
                didCli.add_did(scope=scope, name=dataset, type='DATASET', statuses=None, meta=None, rules=None, lifetime=None)
            except DataIdentifierAlreadyExists:
                pass
            print '| |-', line.rstrip()
            if attachments:
                try:
                    didCli.attach_dids_to_dids(attachments.values())
                    print 'Attached:', attachments.values()
                except Duplicate:
                    pass
                except RucioException as e:
                    if 'IntegrityError' in str(e):
                        pass
                    else:
                        print e
                attachments = {}
            attachment = {'scope':scope, 'name': dataset, 'rse': 'MOCK01', 'dids': [{'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']}]}
            attachments[dataset] = attachment
            previous_dataset = dataset
        elif previous_dataset == dataset:
            print '| |-', line.rstrip()
            attachments[dataset]['dids'].append({'scope':scope, 'name':line.rstrip(), 'bytes':metadata['bytes']})
        else:
            raise Exception('Didn\'t expect this!')
    try:
        print attachments.values()
        didCli.attach_dids_to_dids(attachments.values())
        print 'Attached:', attachments.values()
    except Duplicate as e:
        print e
        pass

if __name__ == '__main__':
    didCli = DIDClient()
    current_dir = os.getcwd()
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('Filename', metavar='File', type=str, help='Filelist')
    parser.add_argument('-s', '--scope', action='store', help='scope of the filelist')
    args = parser.parse_args()
    if not args.scope:
        parser.error('No scope used, add -s')
    else:
        print 'For scope: %s' %(args.scope)
    filelist = args.Filename
    default_struct(filelist, args.scope)
    # single_struct(['1373570791.00000001.root', '1373572204.00000001.root'])


