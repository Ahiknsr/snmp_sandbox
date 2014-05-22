import json
import atexit
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pdu_config
import app_config
import pdu_whisperer


class PduMaster:
    def __init__(self):
        """Setup ui and database, get pdu stats."""
        #When the program exits call the cleanup to clean up curses and the db
        atexit.register(self.cleanup)
        #Read configs
        app_config.read_pdumaster_config()
        self.pdus = pdu_config.read_pdu_config()
        self.pdu_whisperer = pdu_device_whisperer()

    def add_pdu_list(self, pdu_list):
        """Add a list of new pdus to the database"""
        for pdu in pdu_list:
            self.db_session.add(pdu)
        self.db_session.commit()

    def add_pdu(self, new_pdu):
        """Add a new pdu to the database"""
        self.db_session.add(new_pdu)
        self.db_session.commit()

    def update_pdu_list(self, pdus, **fields):
        """Takes a list of pdus as well as *properly* named fields to update"""
        for pdu in pdus:
            self.update(PduUnitModel).where(PduUnitModel.name == pdu.name and
            PduUnitModel.type == pdu.type).values(**fields)
        self.db_session.commit()

    def get_list_of_pdus():
        """Returns a list of pdus from the config"""
        return self.pdus

    def refresh_list_of_pdus():
        """Reloads the pdu config file"""
        self.pdus = pdu_config.read_pdu_config()

    def get_pdu_status(pdu):
        #return self.pdu_whisperer.get_pdu_status(pdu)
        pass

    def turn_off_pdu(pdu):
        #self.whisperer.turn_off_pdu(pdu)
        pass

    def turn_on_pdu(pdu):
        #self.whisperer.turn_on_pdu(pdu)
        pass

    def create_db():
        """Create/connect with the database engine"""
        if app_config.db_engine == None:
            self.engine = create_engine("sqlite:///:memory:")
            pdu_model.Base.metadata.create_all(self.engine)
        else:
            self.engine = create_engine(app_config.db_engine)
        self.db_session = sessionmaker(bind=self.engine)
        init_db()

    def init_db():
        """Query pdus for their properties and commit them to the database"""
        for pdu_key in self.pdus:
            pdu_unit = self.pdu_whisperer.get_pdu_data(pdu_key)
            self.db_session.add(new_pdu)
        self.db_session.commit()

    def cleanup(self):
        """When the program exits clean up the db session"""
        self.db_session.close()
