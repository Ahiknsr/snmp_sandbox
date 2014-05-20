from sqlalchemy.ext.declarative import declarative_base as sql_base

Base = sql_base()

class pdu_unit_model(Base):
    """This class represents a table in the database holding pdu data"""
    __tablename__ = 'pdus'
    pdu_name = Column(String, primary_key=True)
    pdu_type = Column(String, primary_key=True)
    label = Column(String)
    group = Column(String)
    last_updated = Column()

    def __repr__(self):
        """For pretty printing"""
        return "pdu_name %s, sym_name %s, suffix %s, val %i" % (self.name, self.fullname, self.password)
