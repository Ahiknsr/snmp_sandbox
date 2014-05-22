import json

#This is the location of the sqlite3 database engine.
#It must be a string starting with "sqlite:///" or None
db_engine = None

#This is the location of the application config file. it should be a json file
config_file_name = "pdumaster.json"

app_log_level = "debug"

app_log_file = "debug.log"

def read_pdumaster_config():
    """Read in the application configuration from pdumaster.json."""
    global config_file_name
    global db_engine
    global app_log_level
    global app_log_file
    config = open(config_file_name, 'r')
    config_dict = json.load(config)
    config.close()
    db_engine = config_dict.get('db_engine')
    app_log_level = config_dict.get('log_level')
    app_log_file = config_dict.get('log_file')

