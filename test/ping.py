import argcomplete
import argparse
import logging
import os
import random
import sys
import time


from rucio import client
from rucio.client import Client
from rucio import version
from rucio.client.accountclient import AccountClient
from rucio.client.didclient import DIDClient
from rucio.client.replicaclient import ReplicaClient
from rucio.client.metaclient import MetaClient
from rucio.client.pingclient import PingClient
from rucio.client.rseclient import RSEClient
from rucio.client.ruleclient import RuleClient
from rucio.client.scopeclient import ScopeClient
from rucio.client.subscriptionclient import SubscriptionClient
from rucio.common.exception import DataIdentifierAlreadyExists, Duplicate, FileReplicaAlreadyExists, FileAlreadyExists, AccessDenied
from rucio.common.utils import adler32
from rucio.rse import rsemanager as rsemgr

SUCCESS = 0
FAILURE = 1

DEFAULT_SECURE_PORT = 443
DEFAULT_PORT = 80


logger = logging.getLogger("user")
#######################################################
import imp
rucio = imp.load_source('rucio', '/opt/rucio/bin/rucio')
args = argparse.Namespace(account=None, auth_host=None, auth_strategy=None, ca_certificate=None, certificate=None, host=None, password=None, timeout=None, username=None, verbose=False, which='ping')
#rucio.ping(args)
client = PingClient(rucio_host=args.host, auth_host=args.auth_host, account=args.account, auth_type=args.auth_strategy, creds=None, ca_cert=args.ca_certificate, timeout=args.timeout)
print client
