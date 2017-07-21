import MySQLdb

db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity")
cursor = db.cursor()

# Select silenced users
select_comments = """SELECT user_id
                     FROM `tk_activity`.`silenced_users`;"""
comments_results = ''
try:
    cursor.execute(select_comments)
    comments_results = cursor.fetchall()
    print(comments_results)
except:
    print("Error: unable to fecth data")

members_silence = []
if comments_results:
    for each in comments_results:
        members_silence.append(int(each[0]))

print(members_silence)