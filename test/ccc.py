from rucio.client.dq2client import DQ2Client
dq2 = DQ2Client()
#print dq2.listDatasetsByNameInSite('RUCIO-DPM01_TWGRIDSCRATCHDISK')
print dq2.listDatasetsByNameInSite('TW-EOS00_TWGRIDSCRATCHDISK')
