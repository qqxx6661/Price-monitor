#!/usr/bin/env python
# coding:utf-8
import sqlite3


class DatabaseObject(object):
    def __init__(self, db_file):
        self.queries = {
            'SELECT': 'SELECT %s FROM %s',
            'INSERT': 'INSERT INTO %s (%s) VALUES(%s)',
            'UPDATE': 'UPDATE %s SET %s WHERE %s',
            'DELETE': 'DELETE FROM %s where %s',
            'DELETE_ALL': 'DELETE FROM %s',
            'CREATE_TABLE': 'CREATE TABLE IF NOT EXISTS %s(%s)',
        }
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.db_file = db_file
        self.cursor = self.db.cursor()
        self.create_table('proxy')

    def create_table(self, table_name):
        values = '''
           ip varchar(20) NOT NULL,
           port varchar(11) NOT NULL,
           protocol varchar(10) NOT NULL DEFAULT http,
           type int(1) NOT NULL DEFAULT 0,
           area varchar(255) NOT NULL,
           speed int(11) NOT NULL DEFAULT 0,
           updatetime TimeStamp NOT NULL DEFAULT (datetime(\'now\',\'localtime\')),
           lastusedtime TimeStamp NOT NULL DEFAULT '0000-00-00 00:00:00',
           score int(11) DEFAULT 1,
           PRIMARY KEY (ip,port)
       '''
        query = self.queries['CREATE_TABLE'] % (table_name, values)
        self.cursor.execute(query)
        query = '''
           CREATE INDEX IF NOT EXISTS proxy_index on proxy (protocol, type, area, speed, updatetime, lastusedtime, score);
           CREATE TRIGGER IF NOT EXISTS proxy_update_trig AFTER UPDATE OF speed ON proxy
               BEGIN
                 UPDATE proxy SET updatetime=datetime(\'now\',\'localtime\'),score=(score+1) WHERE ip=NEW.ip AND port=NEW.port;
               END;
           CREATE TRIGGER IF NOT EXISTS proxy_insert_trig AFTER INSERT ON proxy
               BEGIN
                 UPDATE proxy SET updatetime=datetime(\'now\',\'localtime\') WHERE ip=NEW.ip and port=NEW.port;
               END;
       '''
        self.cursor.executescript(query)

    def free(self):
        self.cursor.close()

    def select(self, table_name, condition):
        vals = []
        query = self.queries['SELECT'] % (','.join(condition['field']), table_name)
        if condition['where']:
            query += ' WHERE ' + ' and '.join(['%s %s ?' % n[:2] for n in condition['where']])
            vals.extend([n[-1].decode('utf-8') for n in condition['where']])
        if condition['order']:
            query += ' ORDER BY ' + ','.join(condition['order'])
        if condition['limit']:
            query += ' LIMIT ?'
            vals.append(condition['limit'])
        data = self.cursor.execute(query, vals).fetchall()
        return data

    def insert(self, table_name, args):
        result = []
        for arg in args:
            cols = ','.join([k for k in arg])
            values = ','.join(['?' for l in arg])
            vals = tuple([arg[k] for k in arg])
            query = self.queries['INSERT'] % (table_name, cols, values)
            try:
                self.cursor.execute(query, vals)
            except:
                result.append(arg)
        self.db.commit()
        return result

    def update(self, table_name, args):
        result = []
        for arg in args:
            updates = ','.join(['%s=?' % k for k in arg])
            conds = ' and '.join(['%s=?' % k for k in arg if k == 'ip' or k == 'port'])
            vals = [arg[k] for k in arg]
            subs = [arg[k] for k in arg if k == 'ip' or k == 'port']
            query = self.queries['UPDATE'] % (table_name, updates, conds)
            try:
                self.cursor.execute(query, vals + subs)
            except Exception, e:
                print e
                result.append(arg)
        self.db.commit()
        return result

    def executesql(self, query):
        result = self.cursor.execute(query).fetchall()
        self.db.commit()
        return result

    def disconnect(self):
        self.db.close()
