from rucio.client.dq2client import DQ2Client
from rucio.api import lock
dq2 = DQ2Client()
#print dq2.listDatasetsByNameInSite('RUCIO-DPM01_TWGRIDSCRATCHDISK')
#print dq2.listDatasetsByNameInSite('TW-EOS00_TWGRIDSCRATCHDISK')
print lock.get_dataset_locks_by_rse('TW-EOS00_TWGRIDSCRATCHDISK')
