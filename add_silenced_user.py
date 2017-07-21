#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'

import MySQLdb
import sys

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()

silenced_user = sys.argv[1]
print(silenced_user)

if silenced_user:
    sql_add = """INSERT INTO tk_activity.silenced_users(user_id) VALUES (%r);""" % silenced_user
    cursor.execute(sql_add)
    db.commit()
    print("User added into silenced table: "+str(silenced_user))
else:
    print("Nothing was extracted and added to tables")