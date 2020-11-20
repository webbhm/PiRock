import machine
import conf

env_file = "/flash/env.py"

def saveDict(name, file_name, dict):
    f = open(file_name, 'w+')
    tmp = 'env=' + str(dict)
    f.write(tmp)
    f.close()

def create_env():
    env = {}
    location = {}
    location["lat"] = conf.LATITUDE
    location['long'] = conf.LONGITUDE
    env['location'] = location
    env['id'] = machine.unique_id()
    saveDict('env', env_file, env)
        
    