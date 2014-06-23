import requests
#r = requests.get('https://rucio-front03.grid.sinica.edu.tw/ping:443')
r = requests.get('https://rucio-testbed-server.grid.sinica.edu.tw/ping:443', headers = None, verify='/etc/grid-security/certificates/ASGCCA-2007.pem')
print r
