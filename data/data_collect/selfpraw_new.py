import praw
import time
import os
import json
def months_to_seconds(dateback_months=3):
    return dateback_months*30*24*3600

def has_time_efficiency(created_utc, dateback_months=3):
    return time.time() - created_utc <= months_to_seconds(dateback_months)

def submission_in_a_subreddit(subreddit , index_r ,rank_limit=20):
    collect_list=[]
    index_s =0
    for subm in subreddit.hot(limit=rank_limit):

        subm.comments.replace_more(limit=None)# None is better than 0

        #info_dict = info_in_a_submission(subm)
        title = subm.title
        url = subm.url
        time = subm.created_utc
        text = subm.selftext
        info_dict =  {"post_title": title, "post_url": url, "created_utc": time ,'text':text}#https://praw.readthedocs.io/en/stable/
        info_dict['index'] = index_r + 's' + str(index_s) + '_'
        comments_dict = comments_in_a_submission(subm ,info_dict['index'])
        info_dict[list(comments_dict.keys())[0]] = comments_dict[list(comments_dict.keys())[0]]
        collect_list.append(info_dict)

        index_s+=1
    #dump to file
    return collect_list


'''
def info_in_a_submission(submission):
    title = submission.title
    url = submission.url
    time = submission.created_utc
    return  {"post_title":title , "post_url":url, "created_utc":time }
'''


def comments_in_a_submission(submission, index_s):
    Comment_List = []
    index_c =0
    for comment in submission.comments:
        index_comment= index_s+'c'+str(index_c)+'_'
        Comment_List.append({ 'index' :index_comment,
                              "comment_text": submission.selftext,
                             "comment_created_utc":submission.created_utc,
                             "reply_text": comment.body,
                             "reply_created_utc":comment.created_utc })

        # there is a situation where a father  comment body is "deleted" but sons of it are informative
        # so it is better to let below out of the "if"
        Comment_List.extend(replies_in_a_comment( comment , index_comment ))
        index_c+=1
    return { "post_comments" : Comment_List}


def replies_in_a_comment( comment , index_comment):

    reply_list=[]
    FIFO=[]
    FIFO.append([comment , index_comment])

    while FIFO:
        reply = FIFO.pop(0)
        #reply_list.append({ "comment_author":str(reply.author),  "comment_text":reply.body})
        index_r=0
        for one_reply in reply[0].replies:
            index_reply =reply[1]+'r'+str(index_r)+'_'
            reply_list.append({ 'index' : index_reply,
                                "comment_text": reply[0].body,
                               "comment_created_utc": reply[0].created_utc,
                               "reply_text": one_reply.body,
                               "reply_created_utc": one_reply.created_utc
                               })
            index_r+=1
            FIFO.append([one_reply , index_reply])
    return reply_list




''' [updating]
[ # one subreddit
    { "post_title":string   
      "post_url": string    
      "created_utc": time   
      'index' :     
      "post_comments": [         
                            {                              
                                'index' :
                                "comment_text":  string     
                                "comment_created_utc": time
                                "reply_text" : string      
                                reply_created_utc": time
                            }
                            {
                            }...
                       ]
    
    }
    {
    }...
]


'''
def data_check(list_posts): #level-1
    # check data
    for post in list_posts:
        post_checked=[]
        while post["post_comments"]:
            pair=post["post_comments"].pop(0)
            if len(pair['index'].strip('_').split('_')) <= 3:
                post_checked.append(pair)
        post["post_comments"] = post_checked

        '''
        for pair in post["post_comments"]:
            if len(pair['index'].strip('_').split('_'))>3:
                print(pair['index'])
                print(pair)
                post["post_comments"].remove(pair)  # 'remove' will lead to mistake when be with 'for' loop              
            else:
                #print(pair['index'])
                pass
        '''



def cleanse(): # put all conditions here to cleanse data before dump. this will be better
    #if reply.body != '[deleted]' and reply.body != '' and reply.body != None:
    #if has_time_efficiency(reply.created_utc, dateback_months):
    pass

# dump one file with one r/subreddit
def dump_a_subreddit(list_of_posts, subreddit_name, folder_name='dataset'):

    folder_name2 = "notepad_friendly_"+folder_name  # convenient for checking in json format in notepad++
    if os.path.exists(folder_name)==False:
        os.mkdir(folder_name)
    if os.path.exists(folder_name2)==False:
        os.mkdir(folder_name2)
    path = os.path.join( os.getcwd(), folder_name ,f"{subreddit_name}.json")
    path2 = os.path.join(os.getcwd(), folder_name2, f"notepad_friendly_{subreddit_name}.json")
    #print(path)
    with open(path, 'w') as f:
        for submission in list_of_posts:
            f.write(json.dumps(submission) + '\n')

    with open(path2, 'w') as f2:
        json.dump(list_of_posts,f2)

if __name__ == "__main__":
    reddit = praw.Reddit(
        "bot1"
    )
    subr_list =  ['AskEngineers' ,'financialindependence' ,'Entrepreneur' ,'smallbusiness' , 'lifehacks' ,
                  'productivity', 'GetMotivated' ,'GetStudying' ,'Cooking' ,'fantasywriters' ,'WritingPrompts' ,'ShortStories','Jokes']
    #subr = "funny"
    index_r=0
    for subr in subr_list:
        subreddit = reddit.subreddit(subr)
        list_posts = submission_in_a_subreddit(subreddit, 'red' + str(index_r) + '_')
        dump_a_subreddit(list_posts,subr)
        data_check(list_posts)
        dump_a_subreddit(list_posts, subr+'_after_data_check' ,folder_name='dataset_after_data_check' )
        print(subr+' is done')
        index_r+=1

    print('all is done')






