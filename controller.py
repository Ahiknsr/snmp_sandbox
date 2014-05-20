import json
import atexit
import logging

import curses_cli
import db_model
from pdumaster import pdu_device_whisperer

DEBUG = True

class Controller:
    def setup(self):
        """Setup ui and database, get pdu stats."""
        if DEBUG:
            #Enable logging
            logging.basicConfig(filename="debug.log", level=logging.DEBUG)
        else:
            #When the program exits call the cleanup to clean up curses and the db
            atexit.register(self.cleanup)


        pdus = self.read_config()
        logging.debug("PDUs in config: {0}", pdus)

        whisperer = pdu_device_whisperer(pdus)
        create_cli()

        self.db = db_model.db_model(in_memory=True)
        self.db.add_many_pdus(pdumaster.get_stats())

    def create_cli():
        self.cli = curses_cli.curses_cli()
        self.cli.setup()
        self.cli.draw_ui(pdus)

    def cleanup(self):
        """When the program exits clean up changes curses made to the terminal and the db session"""
        self.cli.cleanup()
        print "Sorry, there was an error we couldn't recover from."

if __name__ == '__main__':
    controller = Controller()
    controller.setup()
