import json

def read_pdu_config(config_name=None):
    """Reads a config file (default is ./pdu_config.json), parses it as json and returns the python dictionary it represents"""
    if config_name == None:
        config_name = './pdu_config.json'
    config = open(config_name, 'r')
    config_pdus = json.load(config)
    config.close()
    return  config_pdus
