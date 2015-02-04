from rucio.api.subscription import list_subscriptions, add_subscription, update_subscription, list_subscription_rule_states, get_subscription_by_id
from rucio.client.subscriptionclient import SubscriptionClient
from rucio.common.utils import generate_uuid as uuid

subscription_name = uuid()
result = add_subscription(name=subscription_name, account='root', filter={'project': ['pass4'], 'account': 'root'}, replication_rules=[(1, 'EOS00_AMS02DATADISK', False, True)], lifetime=100000, retroactive=0, dry_run=0, comments='This is a comment')
