#! /usr/bin/env python3
# coding=utf-8
__author__ = 'danilcha'

import MySQLdb
import sys

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity" )
cursor = db.cursor()

if sys.argv[1] == "add":

    silenced_user = sys.argv[2]
    print(silenced_user)

    if silenced_user:
        sql_add = """INSERT INTO tk_activity.SILENCED_USERS(user_id) VALUES (%r);""" % silenced_user
        cursor.execute(sql_add)
        db.commit()
        print("User added into silenced table: "+str(silenced_user))
    else:
        print("Nothing was extracted and added to tables")

elif sys.argv[1] == "del":

    unsilenced_user = sys.argv[2]
    print(unsilenced_user)

    if unsilenced_user:
        sql_remove = """DELETE FROM tk_activity.SILENCED_USERS WHERE user_id = %r;""" % (unsilenced_user)
        cursor.execute(sql_remove)
        db.commit()
        print("User removed from silenced table: "+str(unsilenced_user))
    else:
        print("Nothing was extracted and added to tables")

elif sys.argv[1] == "all":

    select_comments = """SELECT user_id
                         FROM `tk_activity`.`SILENCED_USERS`;"""
    comments_results = ''
    try:
        cursor.execute(select_comments)
        comments_results = cursor.fetchall()
        print(comments_results)
    except:
        print("Error: unable to fecth data")

else:
    print("Usage: \n del 1234567 \n add 1234567 \n all")