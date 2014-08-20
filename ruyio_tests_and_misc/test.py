import requests
#r = requests.get('https://rucio-front03.grid.sinica.edu.tw/ping:443')
r = requests.get('https://chenghsi-rucio-server2.cern.ch/ping:443', headers = None, verify='/etc/grid-security/certificates/CERN-Root-2.pem')
print r
