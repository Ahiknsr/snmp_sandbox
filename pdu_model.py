from sqlalchemy.ext.declarative import declarative_base as sql_base
from sqlalchemy.types import String, DateTime

Base = sql_base()

class PduUnitModel(Base):
    """This class represents a table in the database holding pdu data"""
    __tablename__ = 'pdus'
    name = Column(String, primary_key=True)
    type = Column(String, primary_key=True)
    label = Column(String)
    group = Column(String)
    last_updated = Column()

    def __repr__(self):
        """For pretty printing"""
        return "<PduUnitModel name %s type %s label %s group %s last_updated %s>" % (self.name, self.type, self.label, self.group, self.last_updated)
