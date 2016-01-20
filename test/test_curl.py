import subprocess
import shlex

cacert = '/etc/grid-security/certificates/ASGCCA-2007.pem'
server = 'https://rucio.grid.sinica.edu.tw:443'
x509_proxy = '/tmp/x509up_u500_amspil'
scope = 'ams-2014-ISS.B950-pass6'
dataset = '2011-05-20_01'
name = '1305853512.00000001.root'
account = '\"root\"'
token = ''
# get Rucio token
# cmd = "curl -i --cacert %s -X GET -H \"X-Rucio-Account: root\" -E %s %s/auth/userpass" %(cacert, x509_proxy, server)

class BaseCurl(object):

    def __init__(self):
        get_token = "curl -i --cacert %s -X GET -H \"X-Rucio-Account: %s\" -H \"X-Rucio-Username: ddmlab\" -H \"X-Rucio-Password: secret\" %s/auth/userpass" %(cacert, account, server)
        self.test_curl(get_token)

    def test_curl(self, cmd):
        global token
        prefix = "curl --cacert %s -H \"X-Rucio-Auth-Token: %s\" -s " %(cacert, token)
        cmd = prefix + cmd 
        print cmd
        sub = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None)
        result = sub.communicate()[0]
        if 'userpass' in cmd:
    	    token = result[result.index('X-Rucio-Auth-Token:')+len('X-Rucio-Auth-Token:')+1:result.index('Content-Length')].rstrip()
        print result + '\n'

    

# test_curl(cmd1)


class Scope(BaseCurl):

    def __init__(self):
        BaseCurl.__init__(self)
        print "List available scopes for an account"
        cmd = '-X GET %s/accounts/%s/scopes/' %(server, account)
        self.test_curl(cmd)
        print "List/query all scopes with filter parameter lists"
        cmd2 = ' -X GET %s/scopes/' %(server)
        self.test_curl(cmd2)

class DID(BaseCurl):

    def __init__(self):
        BaseCurl.__init__(self)
        print "Search data identifiers over all scopes with filter parameters"
        cmd = '-X GET %s/dids/' %(server)
        self.test_curl(cmd)
        print "List all data identifiers in a scope"
        cmd = ' -X GET %s/dids/%s/' %(server, scope)
        self.test_curl(cmd)
        # print "List replicas for a data identifier"
        # cmd = ' -X GET %s/dids/%s/?name=%s/rses/' %(server, scope,  name)
        # self.test_curl(cmd)
        print "List content of data identifier"
        cmd = ' -X GET %s/dids/%s/?name=%s' %(server, scope, dataset)
        self.test_curl(cmd)
        # print "List all rules of this did"
        # cmd = ' -X GET %s/dids/%s/%s/rules' %(server, scope,  name)
        # self.test_curl(cmd)
        print " List all keys of the data identifier with their respective values"
        cmd = ' -X GET %s/dids/%s/%s/meta' %(server, scope,  name)
        self.test_curl(cmd)
        print " Get data identifier status"
        cmd = ' -X GET %s/dids/%s/%s/status' %(server, scope,  name)
        self.test_curl(cmd)

class Replica(BaseCurl):

    def __init__(self):
        BaseCurl.__init__(self)
        print "List Replicas of DID"
        cmd = " --data '{\"all_states\": false, \"dids\": [{\"scope\": \"%s\", \"name\": \"%s\"}]}' -X POST %s/replicas/list "  %(scope, name, server)
        self.test_curl(cmd)

x = Replica()

