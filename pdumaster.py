import json
import atexit
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pdu_config
import app_config
import db_model
from pdumaster import pdu_device_whisperer


class PduMaster:
    def setup(self):
        """Setup ui and database, get pdu stats."""
        #Enable logging
        logging.basicConfig(filename="debug.log", level=logging.DEBUG)

        #When the program exits call the cleanup to clean up curses and the db
        atexit.register(self.cleanup)
 
        #Read configs
        app_config.read_pdumaster_config()
        pdus = pdu_config.read_pdu_config()
        logging.debug("PDUs in config: {0}", pdus)
        

        whisperer = pdu_device_whisperer()
        self.cli.draw_ui(pdus)

        self.db = db_model.db_model(in_memory=True)
        self.db.add_many_pdus(pdumaster.get_stats())

    #TODO: Add clean api


    def create_db():
        if app_config.db_engine == None:
            self.engine = create_engine("sqlite:///:memory:")
            #TODO Base needs to be associated with the model somehow
            Base.metadata.create_all(self.engine)
        else:
            self.engine = create_engine(app_config.db_engine)
        self.db_session = sessionmaker(bind=self.engine)

    def cleanup(self):
        """When the program exits clean up the db session"""
		self.db_session.close()

