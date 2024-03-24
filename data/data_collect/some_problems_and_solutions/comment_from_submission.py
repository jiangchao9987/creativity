import praw

# problem has issued and solved in some comments

reddit = praw.Reddit(
    "bot1"  # replaced by your section title in praw.ini or just keyword parameters to put here
)

submission = reddit.submission(url="https://www.reddit.com/r/funny/comments/3g1jfi/buttons/")
print(submission.url) # the output will be different from the inputted url above
submission.comments.replace_more(limit=None)  # tree problem caused by replace_more(limit=None) and its explanation are below
print(len(submission.comments))  # 218
b1 =submission.comments

submission = reddit.submission(url="https://www.reddit.com/r/funny/comments/3g1jfi/buttons/")# should declare again because submision has been used
submission.comments.replace_more(limit=0)
print(len(submission.comments))  # 198
b2 =submission.comments

submission = reddit.submission(url="https://www.reddit.com/r/funny/comments/3g1jfi/buttons/")
print(len(submission.comments)) # 199
b3 =submission.comments

L32=[]  # b3 - b2 ,
L12=[]  # b1 - b2
for i in b3:
    if i not in b2:
        L32.append(i)
print(len(L32)) #1
print(L32)      # just <MoreComment>

for i in b1:
    if i not in b2:
        L12.append(i)
print(len(L12)) # 20
print(L12)


for i in L32:   # details in  L32
    print(len( i.children))  # 23
    for j in i.children:     # 23 = 20 + 3(deleted)
        pass
        #print(reddit.comment(j).body)
        #print('+'*20)
    #print('=' * 20)

#print('*'*20)


Ld=[]  # the children comments of <MoreComment> in L32
       #  -
       #  L12

for i in L32[0].children:
    if reddit.comment(i) not in L12:
        Ld.append(reddit.comment(i))
        print(reddit.comment(i).body)
        #print('+'*20)

print(len(Ld)) #3

'''
[<MoreComments count=35, children=['ctu0791', 'ctuc5sn', 'ctu0lq1', '...']>] 
from replace_more(limit=0)
The <MoreComments> has 35 children, but only 23 can be detected. When zooming in, it can be found that
in these 23, there are 3 comments of "deleted" and 20 also shared by from replace_more(limit=20)
* The rest 12 missing comments, like tutorials said, may come from removed or spam comments
* be careful about "deleted" which will be counted into children list, and "removed" which will not be found anymore 

So, the conclusion is 
for the original comment nodes(199), there may exist <MoreComments>node (here 1)  to including other comments
when using  from replace_more(limit=0) , the infos included in <MoreComments> will be all removed, so the comment nodes in 
top level are 198. 

But when using from replace_more(limit=None)
The good comments (20) in children list from <MoreComments> will be taken into account. So finally, the number of 
comments is 218

* For the rest 15 missing comments from  children list from <MoreComments>, they are 3 "deleted" comments and 12 truly lost
comments, which may refer to removed or spam comments

'''


'''
test
'''
