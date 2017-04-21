# -*- coding: utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(user='root', password='root', database='price-monitor')
cursor = conn.cursor()
cursor.execute('select item_id from monitor')
items = cursor.fetchall()
print items[0]
cursor.close()
conn.close()