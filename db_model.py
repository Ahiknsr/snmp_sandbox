from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
class db_model():
    def __init__(self, in_memory=True):
        """Initialize database connection and possibly create the database in memory"""
        if in_memory:
            self.engine = create_engine("sqlite:///:memory:")
            Base.metadata.create_all(self.engine)
        else:
            # The database is assumed to already exist at ./pdumaster.db
            self.engine = create_engine("sqlite://pdumaster.db")
        self.db_session = sessionmaker(bind=engine)

    def add_many_pdus(self, pdu_list):
        for pdu in pdu_list:
            self.add_pdu_device(pdu) 
        self.db_session.commit()

    def add_pdu_device(self, pdu_name, sym_name, suffix, val):
        new_pdu = pdu_unit_status(pdu_name, sym_name, suffix, val)
        self.db_session.add(new_pdu)
        self.db_session.commit()


    def refresh_certain_db_fields(self, pdus, **fields):
        for pdu in pdus:
            update(self.sql_base).where(pdu_name == pdu).values(**fields)
        #self.db_session.add(new_pdu)
        self.db_session.commit()

    def __del__(self):
        self.db.close()


    
