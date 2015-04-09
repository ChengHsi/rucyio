import json
import sys
import traceback
from rucio.common.exception import Duplicate
from rucio.client import Client
rse_repo_file ='/opt/rucio/etc/rse_repository.json'

json_data = open(rse_repo_file)
repo_data = json.load(json_data)
json_data.close()
c = Client()
for rse in repo_data:
    for p_id in repo_data[rse]['protocols']['supported']:
        try:
            print rse, p_id, repo_data[rse]['protocols']['supported'][p_id]
            c.add_protocol(rse, p_id, params=repo_data[rse]['protocols']['supported'][p_id])
#            c.add_protocol(rse, p_id)
        except ValueError, e:
            print rse, e
        except Duplicate, e:
            continue
        except KeyError:
            continue
        except Exception, e:
            errno, errstr = sys.exc_info()[:2]
            trcbck = traceback.format_exc()
            print 'Interrupted processing for %s with %s %s %s.' % (rse, errno, errstr, trcbck)
