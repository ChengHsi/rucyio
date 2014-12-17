from rucio.client.didclient import DIDClient
from rucio.client.replicaclient import ReplicaClient

rep = ReplicaClient()

rep.list_replicas([{'scope':'ams-2011B-ISS.B620-pass4', 'name':'1340252898.00981893.root'}])

