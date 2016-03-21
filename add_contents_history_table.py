# import sqlalchemy
# sqlalchemy.__version__
from sqlalchemy.engine import create_engine
engine = create_engine('mysql://account:password@db/rucio', echo=True)
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.schema import ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, String, MetaData, Table
from rucio.db.constants import KeyType
from rucio.db.models import ModelBase
# Base = declarative_base()
Base = automap_base()
Base.prepare(engine, reflect=True)
# meta = MetaData()
# meta.reflect(bind=engine)
# scopes = Table('scopes', meta, autoload=True, autoload_with=engine)
class DataIdentifierAssociationHistory(BASE, ModelBase):
    """Represents the map history between containers/datasets and files"""
    __tablename__ = 'contents_history'
    scope = Column(String(25))          # dataset scope
    name = Column(String(255))          # dataset name
    child_scope = Column(String(25))    # Provenance scope
    child_name = Column(String(255))    # Provenance name
    did_type = Column(DIDType.db_type(name='CONTENTS_HIST_DID_TYPE_CHK'))
    child_type = Column(DIDType.db_type(name='CONTENTS_HIST_CHILD_TYPE_CHK'))
    bytes = Column(BigInteger)
    adler32 = Column(String(8))
    md5 = Column(String(32))
    guid = Column(GUID())
    events = Column(BigInteger)
    rule_evaluation = Column(Boolean(name='CONTENTS_HIST_RULE_EVAL_CHK'))
    did_created_at = Column(DateTime)
    deleted_at = Column(DateTime)
    _table_args = (PrimaryKeyConstraint('scope', 'name', 'child_scope', 'child_name', name='CONTENTS_HIST_PK'),
                   CheckConstraint('DID_TYPE IS NOT NULL', name='CONTENTS_HIST_DID_TYPE_NN'),
                   CheckConstraint('CHILD_TYPE IS NOT NULL', name='CONTENTS_HIST_CHILD_TYPE_NN'),
                   Index('CONTENTS_HISTORY_IDX', 'scope', 'name'))

Base.metadata.create_all(engine)
# NamingConvention.metadata.create_all(engine)
