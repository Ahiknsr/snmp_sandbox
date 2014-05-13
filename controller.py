import atexit
import curses_cli
import db_model
import pdumaster

class Controller:
    def setup(self):
        """Setup ui and database, get pdu stats."""
        self.cli = curses_cli.curses_cli()
        self.cli.setup()
        pdus = ('a', 'b')
        self.cli.draw_ui(pdus)
        #When the program exits call the cleanup to clean up curses and the db
        atexit.register(self.cleanup)
        self.db = db_model.db_model(inMemory=True)
        self.db.add_many_pdus(pdumaster.get_stats())


    def cleanup(self):
        """When the program exits clean up changes curses made to the terminal and the db session"""
        self.cli.cleanup()

if __name__ == '__main__':
    controller = Controller()
    controller.setup()
