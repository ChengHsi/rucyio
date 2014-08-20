from rucio.client.didclient import DIDClient  
from rucio.client.dq2client import DQ2Client  
did=DIDClient()
dq2=DQ2Client()

#for x in did.list_files("twgrid-user-testuser1", "TestDataset", long=True):
#    print x

#for x in dq2.listFilesInDataset("TestDataset",scope="twgrid-user-testuser1"):
#    print x
print dq2.listFilesInDataset('TestDataset',0 ,'twgrid-user-testuser1')
print dq2.listFilesInDataset('TestDataset_ROOT',0 ,'twgrid-user-testuser1')

