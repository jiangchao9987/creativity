import praw
import time
import os
import json
def months_to_seconds(dateback_months=3):
    return dateback_months*30*24*3600

def has_time_efficiency(created_utc, dateback_months=3):
    return time.time() - created_utc <= months_to_seconds(dateback_months)



def submission_in_a_subreddit(subreddit, rank_limit , dateback_months=3):
    collect_list=[]
    for subm in subreddit.hot(limit=rank_limit):
        if has_time_efficiency(subm.created_utc,dateback_months):

            subm.comments.replace_more(limit=None)# None is better than 0

            submission_dict = contents_in_a_submission(subm)
            if submission_dict["post_title"]!='' and submission_dict["post_url"]!=''  :
                comments_dict = comments_in_a_submission(subm)
                if  len(comments_dict["post_comments"])!=0:
                    submission_dict[list(comments_dict.keys())[0]] = comments_dict[list(comments_dict.keys())[0]]
                    collect_list.append(submission_dict)


    #dump to file
    return collect_list

def contents_in_a_submission(submission, dateback_months=3):

    title = ''
    url =''
    if submission.selftext!=None and submission.selftext != '[deleted]' and len(submission.selftext) != 0 and submission.selftext != '':
        if has_time_efficiency(submission.created_utc,dateback_months):

            title = submission.title
            print("title:",title)
            url = submission.url
            print("url:", url)

    return  {"post_title":title , "post_url":url}





'''
def comments_in_a_submission(submission, dateback_months=3):
    Comment_List = []
    for comment in submission.comments:
        if comment.body != '[deleted]':
            if has_time_efficiency(comment.created_utc,dateback_months):
                print(comment.author)
                print(comment.body)
                Comment_List.append({ "comment_author":str(comment.author), "comment_text":comment.body})

        # there is a situation where a father  comment body is "deleted" but sons of it are informative
        # so it is better to let below out of the "if"
        Comment_List.extend(replies_in_a_comment(comment))

    return { "post_comments" : Comment_List}
'''
def comments_in_a_submission(submission, dateback_months=3):
    Comment_List = []
    for comment in submission.comments:
        if comment.body != '[deleted]' and len(comment.body) !=0 and comment.body != '' and comment.body != None:
            if has_time_efficiency(comment.created_utc,dateback_months):

                Comment_List.append({"comment_text": submission.selftext, "reply_text": comment.body})
                print({"comment_text_1": submission.selftext, "reply_text": comment.body})


        # there is a situation where a father  comment body is "deleted" but sons of it are informative
        # so it is better to let below out of the "if"
        Comment_List.extend(replies_in_a_comment(comment))

    return { "post_comments" : Comment_List}
'''
def replies_in_a_comment( comment, dateback_months=3):
    FIFO = comment.replies[:]
    reply_list=[]
    while FIFO:
        reply = FIFO.pop(0)
        if reply.body != '[deleted]':
            if has_time_efficiency(reply.created_utc,dateback_months):
                print(reply.author)
                print(reply.body)
                reply_list.append({ "comment_author":str(reply.author),  "comment_text":reply.body})
                FIFO.extend(reply.replies)

    return reply_list
'''

def replies_in_a_comment( comment, dateback_months=3):
    FIFO = comment.replies[:]
    reply_list=[]
    while FIFO:
        reply = FIFO.pop(0)
        if reply.body != '[deleted]' and len(reply.body) !=0 and reply.body !='' and reply.body !=None:
            if has_time_efficiency(reply.created_utc,dateback_months):

                #reply_list.append({ "comment_author":str(reply.author),  "comment_text":reply.body})
                for one_reply in reply.replies:
                    reply_list.append({"comment_text": reply.body, "reply_text": one_reply.body})
                    print({"comment_text_2": reply.body, "reply_text": one_reply.body})

                FIFO.extend(reply.replies)

    return reply_list


''' [obsolete]
{ "post_title":string     --submission title
  "post_url": string      --submission url
  "post_main_text": string   --submission text
  "post_comments": [         --comments belonging to the submission
                        {
                            "comment_author":  string    --author of this comment
                            "comment_text":  string      --text of this comment
                        }
                        {
                        }...
                   ]

}

'''

''' [updating]
{ "post_title":string     --submission title
  "post_url": string      --submission url
  "post_comments": [         
                        {                              
                            "comment_text":  string     #can be text from a submission or a comment
                            "reply_text" : string       #can be a comment              or a reply   
                        }
                        {
                        }...
            ]

}


'''



# dump one file with one r/subreddit
def dump_a_subreddit(list_of_posts, subreddit_name):
    folder_name = 'dataset'
    if os.path.exists(folder_name)==False:
        os.mkdir(folder_name)
    path = os.path.join( os.getcwd(), folder_name ,f"{subreddit_name}.json")
    #print(path)
    with open(path, 'w') as f:
        json.dump(list_of_posts,f)

if __name__ == "__main__":
    reddit = praw.Reddit(
        "bot1"
    )
    subr_list =  ['AskEngineers' ,'financialindependence' ,'Entrepreneur' ,'smallbusiness' , 'lifehacks' ,
                'productivity', 'GetMotivated' ,'GetStudying' ,'Cooking' ,'fantasywriters' ,'WritingPrompts' ,'ShortStories','Jokes']
    #subr = "funny"
    for subr in subr_list:
        subreddit = reddit.subreddit(subr)
        dump_a_subreddit(submission_in_a_subreddit(subreddit,20),subr)



