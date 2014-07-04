from rucio.db.constants import AccountType, IdentityType
from rucio.core.identity import del_identity, del_account_identity
from rucio.client.accountclient import AccountClient
acc = AccountClient()
#del_account_identity('/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', IdentityType.X509, 'chenghsi')
#del_identity('/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', IdentityType.X509)
#acc.del_identity('chenghsi', '/C=TW/O=AS/OU=GRID/CN=Cheng-Hsi Chao 462451', 'x509', 'chenghsi.chao@twgrid.org')
#del_account_identity(identity, type, account, session=None)
#acc.test()


import json
import os
from rucio.common.config import config_get
from rucio.tests.common import account_name_generator, rse_name_generator, execute
def test_get_accounts_whoami():
        """ACCOUNT (CURL): Test whoami method"""
        cmd = 'curl -s -d -i -k --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Account: root" -E /etc/grid-security/hostcert.pem --key /etc/grid-security/hostkey.pem --key-type PEM --ignore-content-length -X GET https://chenghsi-rucio-server2.cern.ch:443/auth/x509' #| grep X-Rucio-Auth-Token' 
        exitcode, out, err = execute(cmd)
        print execute(cmd)
#        nose.tools.assert_in('X-Rucio-Auth-Token', out)
        os.environ['RUCIO_TOKEN'] = out[len('X-Rucio-Auth-Token: '):-1]
        cmd = '''curl -s -i -L --cacert /etc/grid-security/certificates/CERN-Root-2.pem -H "X-Rucio-Auth-Token: $RUCIO_TOKEN" -X GET https://chenghsi-rucio-server2.cern.ch:443/accounts/whoami''' 
        #print '$>' + cmd
        exitcode, out, err = execute(cmd)
        print 'out is', out
#        nose.tools.assert_in('303 See Other', out)
test_get_accounts_whoami()
