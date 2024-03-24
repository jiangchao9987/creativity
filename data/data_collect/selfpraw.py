import praw
import time
import os
import json
def months_to_seconds(dateback_months=3):
    return dateback_months*30*24*3600

def has_time_efficiency(created_utc, dateback_months=3):
    return time.time() - created_utc <= months_to_seconds(dateback_months)


def dump_a_subreddit(list_of_posts, subreddit_name):
    path = os.path.join( f"{subreddit_name}.json")
    with open(path, 'w') as f:
        json.dump(list_of_posts,f)

def submission_in_a_subreddit(subreddit, rank_limit , dateback_months=3):
    collect_list=[]
    for subm in subreddit.hot(limit=rank_limit):
        if has_time_efficiency(subm.created_utc,dateback_months):
            subm.comments.replace_more(limit=None)# None is better than 0
            collect_list.extend(contents_in_a_submission(subm))
            collect_list.extend(comments_in_a_submission(subm))
    #dump to file
    return collect_list

def contents_in_a_submission(submission, dateback_months=3):
    contents=[]
    if submission.selftext!=None:
        if has_time_efficiency(submission.created_utc,dateback_months):
            contents.append(submission.selftext)
            print (submission.selftext)

    return contents

def comments_in_a_submission(submission, dateback_months=3):
    Comment_List = []
    for comment in submission.comments:
        if comment.body != '[deleted]':
            if has_time_efficiency(comment.created_utc,dateback_months):
                print(comment.body)
                Comment_List.append(comment.body)
        # there is a situation where father a comment body is "deleted" but sons of it are informative
        # so it is better to let below out of the "if"
        Comment_List.extend(replies_in_a_comment(comment))

    return Comment_List


def replies_in_a_comment( comment, dateback_months=3):
    FIFO = comment.replies[:]
    reply_list=[]
    while FIFO:
        reply = FIFO.pop(0)
        if reply.body != '[deleted]':
            if has_time_efficiency(reply.created_utc,dateback_months):
                print(reply.body)
                reply_list.append(reply.body)
                FIFO.extend(reply.replies)

    return reply_list

if __name__ == "__main__":
    reddit = praw.Reddit(
        "bot1"
    )
    subr = "funny"
    subreddit = reddit.subreddit(subr)
    dump_a_subreddit(submission_in_a_subreddit(subreddit,20),subr)

