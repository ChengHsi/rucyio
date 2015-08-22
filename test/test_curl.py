import subprocess
import shlex

cacert = '/etc/grid-security/certificates/ASGCCA-2007.pem'
server = 'https://rucio-testbed-server.grid.sinica.edu.tw:443'
x509_proxy = ''
scope = '\"ams-user-chenghsi\"'
name = '\"d1"'
account = 'chenghsi'
cmd = "curl -i --cacert %s -X GET -H \"X-Rucio-Account: root\" -H \"X-Rucio-Username: ddmlab\" -H \"X-Rucio-Password: secret\" %s/auth/userpass" %(cacert, server)
# cmd = "curl -i --cacert %s -X GET -H \"X-Rucio-Account: root\" -E %s %s/auth/userpass" %(cacert, x509_proxy, server)
sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
result = sub.communicate()[0]
token = result[result.index('X-Rucio-Auth-Token:')+len('X-Rucio-Auth-Token:')+1:result.index('Content-Length')].rstrip()

# cmd = "curl --cacert %s -H \"X-Rucio-Auth-Token: %s\" --data '{\"dids\": [{\"scope\": %s, \"name\": %s}]}' -X POST %s/replicas/list " %(cacert, token, scope, name, server)
cmd = "curl --cacert %s -H \"X-Rucio-Auth-Token: %s\" -X GET %s/dids/%s " %(cacert, token, server, scope)
# print cmd
sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
print sub.communicate()[0]
