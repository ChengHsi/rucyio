"""
Register Exist Files

Take a list of dictionaries of files that exist on SE,
add to Rucio DB.
Should be taking a list of JSON files instead?

Ex: python ~/rucyio/file_transfer/register_existfile.py --scope ams-2014-ISS.B950-pass6-sada --se-acrym tw-eos01 --rse TW-EOS01_NONDET_AMS02SCRATCHDISK ~/chchao/rucyio/file_transfer/filelists/tw-eos01-pass6-haino-root-output
"""
import argparse
import os
# from rucio.common.utils import generate_uuid
from rucio.client.replicaclient import ReplicaClient
repCli = ReplicaClient()
import sys
from rucio.client.didclient import DIDClient
didCli = DIDClient()
from rucio.client.ruleclient import RuleClient
ruleCli = RuleClient()
from rucio.client.rseclient import RSEClient
rseCli = RSEClient()
from rucio.common import exception
from filelist_comparator import eos_find2dict
from rucio.common.utils import generate_uuid

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]), add_help=True, description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('Filename', metavar='Filelist', type=str, help='Filelist from eos find on target SE')
    parser.add_argument('--rse', metavar='rse', type=str, help='Target RSE of the filelist, e.g:TW-EOS01_AMS02DATADISK')
    parser.add_argument('--scope', '-s', metavar='Scope', type=str, help='Scope to regisister the files; e.g:ams-2014-ISS.B950-pass6')
    parser.add_argument('--se', metavar='SE', type=str, help='hostname for RSE; e.g:tw-eos01.grid.sinica.edu.tw')
    parser.add_argument('--scheme', metavar='SCH', type=str, help='scheme for pfn; e.g:xroot|s3')
    # parser.add_argument('--prefix', '-p', metavar='Prefix', type=str, help='Prefix of the Directory to register. e.g: /eos/ams/amsdatadisk/, /eos/ams/amsdatadisk/MC/2011B/')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Do a dryrun of the registration.')
    args = parser.parse_args()
    argv_file = args.Filename
    scope = args.scope
    rse_name = args.rse
    se = args.se
    port = '443'
    if args.scheme:
        scheme = args.scheme
    else:
        scheme = 'xroot'
        port = '1094'

    if scheme == 'ark':
        did_dict = eos_find2dict(argv_file, True)
    else:
        did_dict = eos_find2dict(argv_file, False)
    for did in did_dict:
        if scheme == 'ark':
            pfn = did_dict[did]['path']
        else:
            pfn = scheme + '://' + se + ':' + port + '/' + did_dict[did]['path']
        try:
            adler32 = did_dict[did]['adler32']
        except:
            adler32 = None
        try:
            md5 = did_dict[did]['md5']
        except:
            md5 = None
        filename = did_dict[did]['name']
        # filename = name
        bytes = int(did_dict[did]['size'])
        did_dict[did]['guid'] = str(generate_uuid())
        guid = did_dict[did]['guid']

        if args.dry_run:
            print 'pfn:', pfn
            print did_dict[did]
            break

        else:
            try:
                repCli.add_replica(rse_name, scope, filename, bytes, adler32=adler32, pfn=pfn, md5=md5, meta={'guid': guid})
                print 'Replica for %s:%s added' % (scope, filename)
                ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1,
                                             rse_expression=rse_name, grouping='DATASET')
                print 'Rule for %s:%s added' % (scope, filename)
            except exception.Duplicate:
                print 'Already replicated for %s:%s, but try adding rules' % (scope, filename)
                # rules = didCli.list_did_rules(scope=scope, name=filename)
                # rules = didCli.list_associated_rules_for_file(scope=scope, name=filename)
                try:
                    # no_rules4_RSE = True
                    # for x in rules:
                    #     if x['rse_expression'] == rse_name:
                    #         no_rules4_RSE = False
                    #         print 'Already has a rule for the RSE.'
                    #         break
                    #     else:
                    #         continue
                    # if no_rules4_RSE:
                    print 'Has no rules or rules for other RSE, adding rules'
                    ruleCli.add_replication_rule(dids=[{'scope': scope, 'name': filename}], copies=1,
                                                     rse_expression=rse_name, grouping='DATASET')
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            except exception.DuplicateRule:
                print 'Rule already exists'
    try:
        did_dict.close()
    except:
        pass
