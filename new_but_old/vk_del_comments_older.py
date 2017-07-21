#!/usr/local/bin/python3
# coding=utf-8

def delete_comments_older(token, tk_owner_id, tk_group_id, tk_domain, offset):
    from vk_tools.service_functions.logging import log_block_comments
    from time import time, sleep, strftime
    import requests
    import datetime
    import MySQLdb

    db = MySQLdb.connect("localhost","tk_activity","tk_activity","tk_activity")
    cursor = db.cursor()

    # Select silenced users
    select_comments = """SELECT user_id
                         FROM `tk_activity`.`SILENCED_USERS`;"""
    comments_results = ''
    try:
        cursor.execute(select_comments)
        comments_results = cursor.fetchall()
    except:
        log_block_comments("Older deleter - Error: unable to fecth data")

    members_silence = []
    if comments_results:
        for each in comments_results:
            members_silence.append(int(each[0]))

    curr_date = strftime("%d-%m-%Y - %H:%M:%S")
    start = time()

    # log_block_comments("Older deleter - has started it's work")
    # log_block_comments("Older deleter - Offset: "+str(offset))
    error_keys = {'execute_errors', 'error_code', 'error', 'error_msg'}
    # Get Wall posts 100 with offset
    post_id_list = []
    try:
        r_get_posts = requests.post('https://api.vk.com/method/wall.get?owner_id='+tk_owner_id+'&domain='+tk_domain+'&v=5.45&count=100&offset='+str(offset)+'&access_token='+token)
        response_data = r_get_posts.json()
        result = [value for key, value in response_data.items() if key in error_keys]
        if not result:
            data = response_data['response']['items']
            for each in data:
                post_id = each['id']
                comments = each['comments']['count']
                if comments > 0:
                    post_id_list.append(post_id)
        else:
            log_block_comments("Older deleter - "+str(result))
    except:
        log_block_comments("Older deleter - ERROR!!! : Connection ERROR while get wall posts!")

    def replace_all(text, rep_dic):
        for i, j in rep_dic.items():
            text = text.replace(i, j)
        return text

    reps = {"[":"" , " ":"" , "]":"," , "'":""}
    split_by = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

    # Get all comments from posts
    all_comments = []
    if post_id_list:
        # log_block_comments("Get comments from posts: "+" "*26+str(len(post_id_list)))
        splited = split_by(post_id_list, 20)
        item_iteration = 1
        for item in splited:
            # log_block_comments("Iterations were done: "+" "*26+str(item_iteration)+" of "+str(len(splited)))
            item_str = str(item)
            post_list_arg = replace_all(item_str, reps)
            try:
                r = requests.post('https://api.vk.com/method/execute.wall_getComments_parsed?owner_id='+tk_owner_id+'&post_id_array_str='+post_list_arg+'&access_token='+token)
                response_data = r.json()
                result = [value for key, value in response_data.items() if key in error_keys]
                sleep(1)
                if not result:
                    data = response_data['response']
                    all_comments.append(data)
                    item_iteration = item_iteration+1
                else:
                    log_block_comments("Older deleter - "+str(response_data))
            except:
                log_block_comments("Older deleter - ERROR!!! : Connection ERROR while wall_getComments_parsed!")
    else:
        log_block_comments("Older deleter - No posts found!")
    # Format tuple - comment_id, user_id, date, likes
    all_post_comments_formatted = []
    for list_item in all_comments:
        for element in list_item:
            element_formatted = list(zip(element[0],element[1],element[2],element[3]))
            all_post_comments_formatted.append(element_formatted)

    list_of_commet_tuples = []
    # Example: [(481463, 12401695, 1469433603, 0), (481467, 277956638, 1469434029, 0), (481532, 29541596, 1469455778, 0)]
    # Comment_id, user_id, comment_timeDate, likes
    for item in all_post_comments_formatted:
        for each in item:
            list_of_commet_tuples.append(each)

    # print(list_of_commet_tuples)
    # log_block_comments("Older deleter - How many comments: "+" "*32+str(len(list_of_commet_tuples)))
    list_of_users = []
    for user in list_of_commet_tuples:
        if user[1] not in list_of_users:
            list_of_users.append(user[1])

    all_members_not = []
    if list_of_users:
        splited = split_by(list_of_users, 400)
        # log_block_comments("Older deleter - How many users to check: "+" "*26+str(len(list_of_users)))
        item_iteration = 1
        for item in splited:
            # log_block_comments("Older deleter - Iterations were done: "+" "*26+str(item_iteration)+" of "+str(len(splited)))
            sleep(1)
            item_str = str(item)
            user_list_arg = replace_all(item_str, reps)
            try:
                r = requests.post('https://api.vk.com/method/groups.isMember?group_id='+tk_group_id+'&v=5.52&user_ids='+user_list_arg+'&access_token='+token)
                response_data = r.json()
                result = [value for key, value in response_data.items() if key in error_keys]
                if not result:
                    data = response_data['response']
                    for each in data:
                        if each['member'] == 0:
                            all_members_not.append(each['user_id'])
                    item_iteration = item_iteration+1
                else:
                    log_block_comments("Older deleter - "+str(response_data))
            except:
                log_block_comments("Older deleter - ERROR!!! : Connection ERROR while isMember!")
    else:
        log_block_comments("Older deleter - List of members cannot be extracted")

    list_to_delete = []
    # (481558, 266810306, 1469466299, 0)
    if all_members_not:
        log_block_comments("Older deleter - all_members_not ARE: "+str(all_members_not))
        for each in list_of_commet_tuples:
            user_id = each[1]
            if user_id in all_members_not:
                list_to_delete.append(each[0])
                comment_date = datetime.datetime.fromtimestamp(each[2]).strftime('%Y-%m-%d')  # Format time from UNIX to normal
                comment_time = datetime.datetime.fromtimestamp(each[2]).strftime('%H:%M:%S')  # Format time from UNIX to normal
                sql_comments = """INSERT INTO DELETED_COMMENTS(comment_id,comment_user_id,comment_date,comment_time,comment_likes)
                                  VALUES(%s, %s, %r, %r, %s);
                               """ % (each[0],each[1],comment_date,comment_time,each[3])
                cursor.execute(sql_comments)
                db.commit()

    elif members_silence:
        for each in list_of_commet_tuples:
            user_id = each[1]
            if user_id in members_silence:
                log_block_comments("Older deleter - Will delete comment from silenced user: "+str(user_id))
                list_to_delete.append(each[0])
                comment_date = datetime.datetime.fromtimestamp(each[2]).strftime('%Y-%m-%d')  # Format time from UNIX to normal
                comment_time = datetime.datetime.fromtimestamp(each[2]).strftime('%H:%M:%S')  # Format time from UNIX to normal
                sql_comments = """INSERT INTO DELETED_COMMENTS(comment_id,comment_user_id,comment_date,comment_time,comment_likes)
                                  VALUES(%s, %s, %r, %r, %s);
                               """ % (each[0],each[1],comment_date,comment_time,each[3])
                cursor.execute(sql_comments)
                db.commit()
    else:
        log_block_comments("Older deleter - There are no extracted from isUser, stop work!")

    if list_to_delete:
        # log_block_comments("Older deleter - Bot will delete comments: "+" "*26+str(len(list_to_delete)))
        splited = split_by(list_to_delete, 20)
        item_iteration = 1
        for item in splited:
            # log_block_comments("Older deleter - Iterations were done: "+" "*26+str(item_iteration)+" of "+str(len(splited)))
            item_str = str(item)
            comm_list_arg = replace_all(item_str, reps)
            try:
                requests.post('https://api.vk.com/method/execute.deleteComments?owner_id='+tk_owner_id+'&v=5.45&comment_id_array_str='+comm_list_arg+'&access_token='+token)
                item_iteration = item_iteration+1
                sleep(1)
            except:
                log_block_comments("Older deleter - ERROR!!! : Connection ERROR while deleteComments!")
    # else:
        # log_block_comments("Older deleter - Nothing to delete this time"+" "*24+"0")
        db.close()
        end = time()
        log_block_comments("Older deleter - Bot is finishing this iteration! Time spent: "+" "*6+str((end - start)))
        log_block_comments("===========================================================================================")

# Instant run:
# delete_comments_older(token = '14de56889d3a53e072cb6b0823bff9c499fa064f6d057ae8b8f30845aeb2c9388b45e303131057259034c', tk_owner_id = "-46631810" , tk_group_id = "46631810", tk_domain = "typical_kirovohrad", offset=19)