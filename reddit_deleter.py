import praw
from datetime import datetime, timezone

account = input("Which account? (no /u)")
sub = input("Which subreddit? (no r/), 'all' for everthing")
comment_count = int(input("How many comments?"))
action = input("edit or delete?")

def authenticate(account):
    """
    Authenticate with Reddit's API using account.
    """
    r = praw.Reddit(account)
    r.validate_on_submit = True
    print(f'Authenticated as {r.user.me()}')
    return r

def get_comments(r, subreddit, limit = comment_count):
    """
    Get the most recent 20 comments from my account. Store in a list of dicts.

    praw comment objects are generators, so be sure to populate list of dicts on first iteration.
    """
    print(f'Getting recent {limit} comments from {r.user.me()}.')
    c = r.user.me().comments.new(limit = limit)
    comments = []
    for i in c: # remember that iterating through a comment object clears the comment object because it's a generator
        if i.subreddit.display_name == subreddit or subreddit == 'all':
            comment = {}
            time = datetime.fromtimestamp(i.created_utc, timezone.utc).strftime('%Y-%m-%d')

            comment['id'] = i.id
            comment['subreddit'] = i.subreddit.display_name
            comment['created_on'] = time

            comments.append(comment)

            print(f'{i.id} - {i.subreddit.display_name} - {time}')
    return comments

def edit_comments(r, comments):
    """
    Replace a comment's text with gibberish.
    """
    togo = len(comments)
    for i in comments:
        print(f"Comment on {i['created_on']} was:\n {r.comment(i['id']).body}")
        r.comment(i['id']).edit('Whoopsies! 404 comment not found.')
        print(f"Comment is now {r.comment(i['id']).body}")
        togo-=1
        print(f"{togo} comments left to edit.\n")

def delete_comments(r, comments):
    """
    Call each comment and delete it.
    """
    togo = len(comments)
    for i in comments:
        print(f"Deleting from {i['created_on']}: {r.comment(i['id']).body}")
        r.comment(i['id']).delete()
        togo-=1
        print(f"{togo} comments left to go.\n")

if __name__ == '__main__':
    r = authenticate(account)
    c = get_comments(r, sub, limit = comment_count)
    if action == 'edit':
        edit_comments(r, c)
    elif action == 'delete':
        delete_comments(r, c)
    else:
        print('Invalid action. edit or delete. Try again.')