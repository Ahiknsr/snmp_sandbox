import json
import atexit
import logging

import curses_cli
import db_model
import pdumaster

DEBUT = True

class Controller:
    def setup(self):
        """Setup ui and database, get pdu stats."""
        #When the program exits call the cleanup to clean up curses and the db
        atexit.register(self.cleanup)
        if DEBUG:
            logging.basicConfig(filename="debug.log", level=logging.DEBUG)

        self.cli = curses_cli.curses_cli()
        self.cli.setup()

        pdus = read_config()
        logging.debug("PDUs in config: {0}", pdus)

        whisperer = pdu_device_whisperer(pdus)

        self.cli.draw_ui(pdus)
        self.db = db_model.db_model(inMemory=True)
        self.db.add_many_pdus(pdumaster.get_stats())

    def read_config(config_name=None):
        """Reads a config file (default is ./osuosl_pdus.conf), parses it as json and returns the python dictionary it represents"""
        if config_name != None:
            controller = './osuosl_pdus.conf'
        config = open(controller, 'r')
        config_pdus = json.load(config)
        config.close()
        return  config_pdus


    def cleanup(self):
        """When the program exits clean up changes curses made to the terminal and the db session"""
        self.cli.cleanup()
        print "Sorry, there was an error we couldn't recover from."

if __name__ == '__main__':
    controller = Controller()
    controller.setup()
