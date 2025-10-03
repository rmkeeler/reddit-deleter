import praw
from datetime import datetime, timezone

account = input("Which account? (no /u)")
subreddit = input("Which subreddit? (no r/), 'all for everthing'")

def authenticate():
    """
    Authenticate with Reddit's API using account.
    """
    r = praw.Reddit(account)
    r.validate_on_submit = True
    print(f'Authenticated as {r.user.me()}')
    return r

def get_comments(r, subreddit, limit = 20):
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
    for i in comments:
        r.comment(i['id']).edit('Scrambled eggs and bacon make me thirsgry.')
        print(f'Comment was {r.comment['id'].body}')