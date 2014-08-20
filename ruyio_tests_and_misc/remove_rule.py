import sys, subprocess
from rucio.client.ruleclient import RuleClient
ruleCli = RuleClient()
argv_file =str(sys.argv[1])
with open(argv_file, 'r') as rule_ids:
    for rule_id in rule_ids:
        rule_id = rule_id.rstrip('\n')
        #ruleCli.delete_replication_rule(rule_id)
        print rule_id
        subprocess.check_call(['/opt/rucio/bin/rucio', 'delete-rule', rule_id])


#ruleCli.delete_replication_rule('7FD5E09C3B6243758494235B6D6E3EAE')
