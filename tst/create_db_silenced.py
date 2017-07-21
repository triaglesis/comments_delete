#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'
# Change history

import MySQLdb

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity")

# Connection to database establish here:
# Like as vkapi
cursor = db.cursor()
# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS SILENCED_USERS")

sql = """CREATE TABLE SILENCED_USERS(
         user_id CHAR(20) NOT NULL PRIMARY KEY
         )"""
# Execute previous command:
cursor.execute(sql)
# disconnect from database server and close cursor!
db.close()