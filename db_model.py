import sqlite3

_pdu_schema = """
create table pdus(
    --stuff here
);
"""
#TODO refactor this out into its own class
class pdu_unit_status():
    def __init__(self):
        raise NotImplementedError
        self.pdu_name = ""
        self.stuff = "stuff"


class db_model():
    def __init__(self, in_memory=True):
        """Initialize database connection, and possibly the database in memory"""
        if in_memory:
            self.db_conn = sqlite3.connect(":memory:")
            _create_tables()
        else:
            self.db_conn = sqlite3.connect("pdumaster.db")
        self.db_cursor = self.db_conn.cursor()

    def add_pdu_device(self, data):
        raise NotImplementedError
        pass

    def refresh_certain_db_fields(self, pdu, **fields):
        raise NotImplementedError
        pass
    
    def _create_tables(self):
        self.db_cursor.execute(_pdu_schema) 
