from rucio.db import models
from rucio.db.session import read_session, transactional_session, stream_session
from rucio.db.constants import DIDType
from rucio.common import exception
from rucio.client.didclient import DIDClient
dc = DIDClient()
import sys
# # remove client rucio path and use /opt/rucio/lib as server path
# sys.path.insert(0, '/opt/rucio/lib/')
# sys.path.remove('/opt/rucio/.venv/lib/python2.6/site-packages/rucio-0.2.5_15_g2289bda_dev1416935547-py2.6.egg')
# del sys.modules['rucio']
# # import imp
# # rucio = imp.load_source('rucio','/opt/rucio/lib/rucio/__init__.py')
# from rucio.api.did import get_did


# print get_did('ams-user-chenghsi', 'd2')
# dc.detach_dids('ams-user-chenghsi', 'd1', ['file3'])
# dc.non_attached('ams-user-chenghsi', [{'scope':'ams-user-chenghsi', 'name':'file1'}, {'scope':'ams-user-chenghsi', 'name':'file2'}])
print dc.non_attached('twgrid-user-chenghsi', [{'scope':'ams-user-chenghsi', 'name':'file1'}, {'scope':'twgrid-user-chenghsi', 'name':'file2'}, {'scope':'twgrid-user-chenghsi', 'name':'file6'}, {'scope':'twgrid-user-chenghsi', 'name':'file1'}])
# print dc.non_attached('ams-user-chenghsi', ['file1', 'name':'file2'}])
# @stream_session
@read_session
def non_attached(scope, names, session=None):
    """
    List data identifier contents.

    :param scope: The scope name.
    :param names: The data identifier name.
    :param session: The database session in use.
    """
    attached_dids = []
    detached_dids = []
    file = DIDType.from_sym('FILE')
    try:
        query = session.query(models.DataIdentifierAssociation).filter_by(scope=scope)
        # query2 = session.query(models.DataIdentifier).filter_by(scope=scope, did_type=file)
        for tmp_did in query.yield_per(5):
            attached_dids.append(tmp_did.child_name)
        for name in names:
            if name not in attached_dids:
                detached_dids.append(name)
        # for tmp_did in query2.yield_per(5):
        #     dids_full.append(tmp_did.name)
        # return {'non_attached':list(set(dids_full) - set(dids))}
        return {'non_attached':detached_dids}
    except:
        raise

# print non_attached('ams-user-chenghsi', ['file1', 'file2', 'file3', 'file4'])

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



