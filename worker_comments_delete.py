#!/usr/local/bin/python3
# coding=utf-8

from time import strftime, sleep, time
import schedule
from comments_delete.vk_del_comments import del_comments_regular
from comments_delete.vk_del_comments_older import delete_comments_older
import os

# pid = os.getpid()
# op = open("/var/us.pid","w")
# op.write("%s" % pid)
# op.close()

token = '14de56889d3a53e072cb6b0823bff9c499fa064f6d057ae8b8f30845aeb2c9388b45e303131057259034c'
tk_owner_id = "-46631810"
tk_group_id = "46631810"
tk_domain = "typical_kirovohrad"
# tk_owner_id = "-80849532"
# tk_group_id = "80849532"
# tk_domain = "scandal_kir"
# offset = ""

curr_date = strftime("%d-%m-%Y - %H:%M:%S")
logFile = 'comments_deleter_log.txt'

# print("Start Comments Bot Worker!")
def log_block(message):
    with open(logFile, "a", encoding='utf-8') as f:
        f.write(curr_date+" WORKER: -> "+message+"\n")

def del_comments_fast():
    try:
        del_comments_regular(logFile, token, tk_owner_id, tk_group_id, tk_domain)
    except:
        log_block("ERROR!!! : Connection error!")

def del_comments_offset(offset, sleep_time):
    print("Func 1 min start")
    start = time()
    try:
        sleep(sleep_time)
        delete_comments_older(logFile, token, tk_owner_id, tk_group_id, tk_domain, offset)
        end = time()
        print("Func 1 min time spent: "+" "*6+str((end - start)))
    except:
        log_block("ERROR!!! : Connection error!")

# def del_offset_comments():
#     print("Func 30 mins start")
#     start = time()
#     offsets = [119,220,321,422,523,624,725,826,927,1028,1129,1230]
#     sleeping = 0
#     for offset in offsets:
#         del_comments_offset(offset=offset, sleep_time=sleeping)
#         sleeping = sleeping + 1
#     end = time()
#     print("Func 30 mins time spent: "+" "*6+str((end - start)))

# schedule.every(30).seconds.do(del_comments_fast)
# schedule.every(30).seconds.do(del_comments_offset, offset=19, sleep_time=0)
# schedule.every(5).minutes.do(del_offset_comments)
del_comments_fast()
del_comments_offset(offset=19, sleep_time=0)

# while True:
#     schedule.run_pending()
#     sleep(1)