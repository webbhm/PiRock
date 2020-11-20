"""
THe purpose of this code is to call the test functions of the high level modules for a quick check that all is working correctly

Author: Howard Webb
Data: 11/13/2020

""""
def test():
    # High level test
    import LogSensors
    LogSensors.test()

# parameter files do not have their own test
def conf_test():
    # Dump the configuration parameters

    print("\nconf.py test")
    try:
        import conf
        print("SSID", conf.SSID)
        print("PWD", conf.PWD)
        print("START_TIME", conf.START_TIME)
        print("SAMPLE_MIN", conf.SAMPLE_MIN)
        print("conf test: PASS")
    except Exception as e:
        # Print error in RED
        print("/033[1;31;40m ERROR: Failed conf test - ", str(e))

def env_test():
    print("\n env test")
    try:
        import env


        print(env)
        print("env test: PASS")
    except Exception as e:
        print("ERROR: Failed env test - ", str(e))


def detail_test():
    # most modules have their own test
    print("\n Test configuration files")
    conf_test()
    env_test()

    print("\n Test sensors")    
    import BME280
    BME280.test()

    import Turbidity()
    Turbidity.test()

    import EC
    EC.test()

    print("\n High level functions")
    test()

    

    
    