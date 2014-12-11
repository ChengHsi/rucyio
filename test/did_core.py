from rucio.db import models
from rucio.db.session import read_session, transactional_session, stream_session
from rucio.db.constants import DIDType
from rucio.common import exception
from rucio.client.didclient import DIDClient
dc = DIDClient()
from rucio.api.did import get_did
import pdb;pdb.set_trace()
print get_did('ams-user-chenghsi', 'd2')
# print dc.non_attached('ams-user-chenghsi')
# @stream_session
@read_session
def non_attached(scope, session=None):
    """
    List data identifier contents.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param session: The database session in use.
    """
    dids = [] 
    dids_full = []
    file = DIDType.from_sym('FILE')
    try:
        query = session.query(models.DataIdentifierAssociation).filter_by(scope=scope)
        query2 = session.query(models.DataIdentifier).filter_by(scope=scope, did_type=file)
        for tmp_did in query.yield_per(5):
            dids.append(tmp_did.child_name)
        for tmp_did in query2.yield_per(5):
            dids_full.append(tmp_did.name)
        return list(set(dids_full) - set(dids))
 
    except:
        raise
# non_attached('ams-user-chenghsi','d1')
print non_attached('ams-user-chenghsi')

@read_session
def get_did(scope, name, session=None):
    """
    Retrieve a single data identifier.

    :param scope: The scope name.
    :param name: The data identifier name.
    :param session: The database session in use.
    """
    try:
        r = session.query(models.DataIdentifier).filter_by(scope=scope, name=name).one()
        if r.did_type == DIDType.FILE:
            did_r = {'scope': r.scope, 'name': r.name, 'type': r.did_type, 'account': r.account}
        else:
            did_r = {'scope': r.scope, 'name': r.name, 'type': r.did_type,
                     'account': r.account, 'open': r.is_open, 'monotonic': r.monotonic, 'expired_at': r.expired_at,
                     'length': r.length, 'bytes': r.bytes}
        return did_r
    except NoResultFound:
        raise exception.DataIdentifierNotFound("Data identifier '%(scope)s:%(name)s' not found" % locals())



# print get_did('ams-user-chenghsi', 'AUTHORS')



