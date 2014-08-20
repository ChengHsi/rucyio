import json
import sys
import re
import uuid
import hashlib

from datetime import datetime, timedelta
from nose.tools import raises

from sqlalchemy import *
from sqlalchemy.orm.exc import *

from rucio.api import did
from rucio.api import scope
from rucio.db.constants import DIDType
from rucio.client.accountclient import AccountClient
from rucio.client.metaclient import MetaClient
from rucio.client.rseclient import RSEClient
from rucio.client.scopeclient import ScopeClient
from rucio.client.ruleclient import RuleClient
from rucio.common.exception import (DataIdentifierNotFound, DataIdentifierAlreadyExists,
                                    KeyNotFound, UnsupportedOperation, UnsupportedStatus, ScopeNotFound)
from rucio.common.utils import generate_uuid
from rucio.tests.common import rse_name_generator, scope_name_generator

from rucio.api.subscription import list_subscriptions, add_subscription
from rucio.api.rule import add_replication_rule
from rucio.client.didclient import DIDClient
from rucio.client.subscriptionclient import SubscriptionClient
from rucio.common.exception import SubscriptionDuplicate
from rucio.common.exception import InvalidReplicationRule
from rucio.client.rseclient import RSEClient
from rucio.client.fileclient import FileClient

def main(argv):
    try:
        did_client=DIDClient()
        rule_client=RuleClient()
        openfile_name = sys.argv[1]
        scope_name = 'twgrid-user-wchang'
        mysql_engine = create_engine("mysql://root:asgcddm@rucio-db01.grid.sinica.edu.tw/rucio")
        with open(openfile_name) as file:
            for line in file:
                connection = mysql_engine.connect()
                data=line.strip('\n')
                dataset=data.split(" ")[0]
                file_name=data.split(" ")[1]
                file_size=int(data.split(" ")[2])
                account=data.split(" ")[3]
                pre_md5='twgrid-user-wchang:'+file_name
                md5_sum = hashlib.md5(pre_md5).hexdigest()
                files = []
                files.append({'scope': scope_name, 'name': file_name, 'md5':md5_sum, 'bytes':file_size, 'adler32':'0cc737eb'})
                contact_db = connection.execute("select * from dids where scope='%s' and name='%s';"%(scope_name, file_name)) 
            
                num_rows = contact_db.rowcount
                if num_rows == 0:
                    print "Register File : %s "%file_name 
                    did_client.add_files_to_dataset(scope=scope_name, name=dataset, files=files, rse='TW-DPM01_TWGRIDSCRATCHDISK')
                    #rule_client.add_replication_rule(dids=[{'scope': scope_name, 'name': file_name}], account=account, copies=1, \
                    #                                 rse_expression='TW-DPM01_TWGRIDSCRATCHDISK', grouping='DATASET')
                else:
                    print "Attach File : %s To %s "%(file_name, dataset)
                    did_client.attach_dids(scope=scope_name, name=dataset, dids=files)

                connection.close()                
 
    except SubscriptionDuplicate, e:
        print e

if __name__ == '__main__':
    main(sys.argv[1:])
