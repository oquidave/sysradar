'''
Created on Aug 13, 2011

@author: oquidave
'''
import psycopg2
# import psycopg2.extras
class DbHandler(object):
    '''
    this creates a postgres database hanlder for any host
    '''
    def __init__(self, host, dbname):
        '''
        Constructor
        '''
        self.host = host
        self.dbname = dbname
        dbh_stg = "host='%s' user='postgres' dbname='%s'" % (self.host, self.dbname)
        dbh = psycopg2.connect(dbh_stg)
        return dbh
        
