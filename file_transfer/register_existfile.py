"""
Register Exist Files

Take a list of dictionaries of files that exist on SE,
add to Rucio DB.
Should be taking a list of JSON files instead?
"""

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
from eosd import eos_find2dict


argv_file = str(sys.argv[1])
# scope = 'ams-2011B-ISS.B620-pass4'
prefix = '/eos/ams/amsdatadisk/'
# prefix = '/eos/ams/amsdatadisk/MC/2011B/'
try:
    rse_name = str(sys.argv[2])
except:
    if 'tw-eos01' in sys.argv[1]:
        rse_name = 'TW-EOS01_AMS02DATADISK'
    elif 'tw-eos02' in sys.argv[1]:
        rse_name = 'TW-EOS02_AMS02DATADISK'
    elif 'tw-eos03' in sys.argv[1]:
        rse_name = 'TW-EOS03_AMS02DATADISK'
import pdb; pdb.set_trace()
did_dict = eos_find2dict(argv_file)
for did in did_dict:
    # md5 = unicode(did_list[3])
    # pfn = prefix + scope + '/' + filename
    scope = did_dict[did]['scope']
    pfn = 'xroot://tw-eos03.grid.sinica.edu.tw:1094/' + did_dict[did]['path']
    adler32 = did_dict[did]['adler32']
    filename = did_dict[did]['name']
    bytes = int(did_dict[did]['size'])
    # did['md5'] = None
    # did_dict[did]['guid'] = str(generate_uuid())
    # print did_dict[did]
    # break
    try:
        repCli.add_replica(rse_name, scope, filename, bytes, adler32, pfn)
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
