import sys
sys.path.insert(0, '/root/.virtualenvs/rucio/lib/python2.6/site-packages/rucio-0.1.29-py2.6.egg/rucio/core/')
import authentication as auth
sys.path.insert(2, '/root/.virtualenvs/rucio/lib/python2.6/site-packages/rucio-0.1.29-py2.6.egg/rucio/api')
import authentication as api_auth
sys.path.insert(1, '/root/.virtualenvs/rucio/lib/python2.6/site-packages/rucio-0.1.29-py2.6.egg/rucio/db')
import session
print api_auth.get_auth_token_user_pass('root', 'ddmlab', 'secret', 1, '128.142.141.180')
#auth = authentication
#auth.exist_identity_account = session.transactional_session(auth.exist_identity_account('ddmlab', 'USERPASS', 'root'))
#print auth.exist_identity_account('ddmlab@CERN.CH', str("GSS"), 'root', session=None)
#print a
#print api_auth.get_auth_token_user_pass('root', 'ddmlab', 'shit', 1, '128.142.141.180')
