#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'

import MySQLdb
import sys

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()

unsilenced_user = sys.argv[1]
print(unsilenced_user)

if unsilenced_user:
    sql_remove = """DELETE FROM tk_activity.silenced_users WHERE user_id = %r;""" % (unsilenced_user)
    cursor.execute(sql_remove)
    db.commit()
    print("User removed from silenced table: "+str(unsilenced_user))
else:
    print("Nothing was extracted and added to tables")