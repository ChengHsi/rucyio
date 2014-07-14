from rucio.db.constants import AccountType, IdentityType
from rucio.core.identity import del_identity, del_account_identity
from rucio.client.accountclient import AccountClient
import json
import os
import nose
from rucio.common.config import config_get
from rucio.tests.common import account_name_generator, rse_name_generator, execute
#acc = AccountClient()
#del_account_identity('/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', IdentityType.X509, 'chenghsi')
#del_identity('/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', IdentityType.X509)
#acc.del_identity('chenghsi', '/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', 'x509', 'chenghsi.chao@twgrid.org')
#del_account_identity(identity, type, account, session=None)
#acc.test()
#cmd = '''curl -s -i -d -k -L --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Auth-Token: root-ddmlab-unknown-deab467bf2ef49e5bbc6a161f88b17cc" -X GET https://chenghsi-rucio-server2.cern.ch:443/identities/x509'''
#exitcode, out, err = execute(cmd)
#print 'out is', out

class testCurl():
    def setup(self):
        self.host = config_get('client', 'rucio_host')
        self.auth_host = config_get('client', 'auth_host')
#        print 'get from config:', self.host, self.auth_host
        self.marker = '$> '
    def test_get_accounts_whoami(self):
        """ACCOUNT (CURL): Test whoami method"""
        cmd = 'curl -s -d -i -k -L --verbose --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Account: root" -E /etc/grid-security/hostcert.pem --key /etc/grid-security/hostkey.pem --key-type PEM --ignore-content-length -X GET https://chenghsi-rucio-server2.cern.ch:443/auth/x509' 
        exitcode, out, err = execute(cmd)
        #nose.tools.assert_in('X-Rucio-Auth-Token', out)
        os.environ['RUCIO_TOKEN'] = err[len('X-Rucio-Auth-Token: '):-1]
        #print os.environ['RUCIO_TOKEN']
        print err[err.find('X-Rucio-Auth-Token'):]
        nose.tools.assert_in('X-Rucio-Auth-Token', err)
        #print out
        #cmd = '''curl -s -i -d -k -L --verbose --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Auth-Token: root-/DC=ch/DC=cern/OU=computers/CN=chenghsi-rucio-server2.cern.ch-unknown-aef0d8c555974ef7888a7ae168c05993" -E /etc/grid-security/hostcert.pem --key /etc/grid-security/hostkey.pem --key-type PEM --ignore-content-length -X GET https://chenghsi-rucio-server2.cern.ch:443/accounts/whoami''' 
        #cmd = '''curl -s -i -d -k -L --verbose --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Auth-Token: root-/DC=ch/DC=cern/OU=computers/CN=chenghsi-rucio-server2.cern.ch-unknown-aef0d8c555974ef7888a7ae168c05993" -E /etc/grid-security/hostcert.pem --key /etc/grid-security/hostkey.pem --key-type PEM --ignore-content-length -X GET https://chenghsi-rucio-server2.cern.ch:443/accounts/whoami''' 
        #cmd = '''curl -s -i -d -k -L --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Auth-Token: $RUCIO_TOKEN" -X GET https://chenghsi-rucio-server2.cern.ch:443/accounts/whoami'''
        #print self.marker + cmd
        #exitcode, out, err = execute(cmd)
        #print exitcode, out
        #print 'out is', out
    #    nose.tools.assert_in('303 See Other', out)
#print acc.get_account('whoami')
#print acc.whoami
testC = testCurl()
testC.setup()
testC.test_get_accounts_whoami()
#https://chenghsi-rucio-server2.cern.ch:443/accounts/whoami



