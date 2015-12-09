"""
Register Exist Files

Take a list of dictionaries of files that exist on SE,
add to Rucio DB.
Should be taking a list of JSON files instead?
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
    parser.add_argument('--se-acrym', '-sa', metavar='SE', type=str, help='se name for pfn; e.g:tw-eos01')
    # parser.add_argument('--prefix', '-p', metavar='Prefix', type=str, help='Prefix of the Directory to register. e.g: /eos/ams/amsdatadisk/, /eos/ams/amsdatadisk/MC/2011B/')
    args = parser.parse_args()
    argv_file = args.Filename
    scope = args.scope
    rse_name = args.rse
    se = args.se_acrym
    did_dict = eos_find2dict(argv_file)
    for did in did_dict:
        # md5 = unicode(did_list[3])
        # pfn = prefix + scope + '/' + filename
        # scope = did_dict[did]['scope']
        # import pdb ;pdb.set_trace()
        pfn = 'xroot://' + se + '.grid.sinica.edu.tw:1094/' + did_dict[did]['path']
        adler32 = did_dict[did]['adler32']
        filename = did_dict[did]['name']
        bytes = int(did_dict[did]['size'])
        # did['md5'] = None
        did_dict[did]['guid'] = str(generate_uuid())
        guid = did_dict[did]['guid']
        # import pdb; pdb.set_trace()
        # print did_dict[did]

        # break
        try:
            # import pdb; pdb.set_trace()
            repCli.add_replica(rse_name, scope, filename, bytes, adler32, pfn, meta={'guid': guid}) 
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
