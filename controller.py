import curses_cli
import db_model
import pdumaster

class Controller:
    def setup():
        """Setup ui and database, get pdu stats."""
        pdumaster.start_ui()
        #When the program exits call the cleanup to clean up curses and the db
        atexit.register(cleanup)
        db_model.initdb(in_memory=True)
        db_model.get_stats(pdumaster.get_stats())

    def cleanup():
        """When the program exits clean up changes curses made to the terminal and the db session"""
        curses_cli.cleanup()
        db_model.cleanup()

if __name__ == '__main__':
    controller = Controller()
    controller.setup()
