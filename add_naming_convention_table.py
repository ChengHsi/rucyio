# import sqlalchemy
# sqlalchemy.__version__
from sqlalchemy.engine import create_engine
engine = create_engine('mysql://root:asgcddm@rucio-testbed-server.grid.sinica.edu.tw/rucio', echo=True)
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
class NamingConvention(Base, ModelBase):
    """Represents naming conventions for name within a scope"""
    __tablename__ = 'naming_conventions'
    scope = Column(String(25))
    regexp = Column(String(255))
    convention_type = Column(KeyType.db_type(name='CVT_TYPE_CHK'))
    _table_args = (PrimaryKeyConstraint('scope', name='NAMING_CONVENTIONS_PK'), ForeignKeyConstraint(['scope'], ['scopes.scope'], name='NAMING_CONVENTIONS_SCOPE_FK'))

Base.metadata.create_all(engine)
# NamingConvention.metadata.create_all(engine)
