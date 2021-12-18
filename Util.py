from os import environ

class Util:

    def writeEnvVar(key,value):
        file_object = open('.env', 'a')
        file_object.write(key+'='+value)
        file_object.close()