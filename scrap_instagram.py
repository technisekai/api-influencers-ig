import instaloader          #scrapping ig
from save_to_db import *
import re
from datetime import date 


today = date.today().strftime("%Y-%m-%d")
bot = instaloader.Instaloader()

# check if account is found in instagram, return obj or bool
def is_account_found(username):
    account = False
    try:
        account = instaloader.Profile.from_username(bot.context, username)
    except:
        account = False
    return account

# calculating ER
def calc_er(total_likes, total_comments, total_posts, total_followers):
    avg_likes = total_likes / total_posts
    avg_comments = total_comments / total_posts
    result = ((avg_likes + avg_comments) / total_followers) * 100
    return result

# scrap posts information from username given
def scrap_posts_data(account):
    username = account.username
    results = []
    posts = account.get_posts()
    for post in posts:
        result = {}
        result['date_scrap'] = today
        result['username'] = username
        result['post_date'] = post.date.strftime("%Y-%m-%d")
        result['shortcode'] = post.shortcode
        result['caption'] = re.sub("[^a-zA-Z0-9 ]", "", str(post.caption))
        result['count_likes'] = post.likes if post.likes >= 0 else 0
        result['count_comments'] = post.comments
        results.append(result)
    return results

# scrap basic information from username given
def scrap_basic_data(account, posts_information):
    results = {}
    total_likes, total_comments = 0, 0
    # find total likes and comments
    for post in posts_information:
        total_likes += post['count_likes']
        total_comments += post['count_comments']
    
    results['date_scrap'] = today
    results['username'] = account.username
    results['followers'] = account.followers
    results['following'] = account.followees
    results['total_posts'] = account.mediacount
    results['total_likes'] = total_likes
    results['total_comments'] = total_comments
    results['engagment_rate'] = calc_er(
        total_likes, 
        total_comments, 
        account.mediacount,
        account.followers
        )
    return results

# the main function to scrap and save into database
def main(username):
    account = is_account_found(username)
    if account:
        count_posts = account.mediacount
        is_private_account = account.is_private
        # if account is public and any post in account, return information
        if not is_private_account and count_posts:
            posts_information = scrap_posts_data(account=account)
            basic_information = scrap_basic_data(
                account=account, 
                posts_information=posts_information
            )
            insert_to_basic_db(basic_information)
            insert_to_post_db(posts_information)
        else: print('{username} account is private or not having posts, skipped'.format(username=username))
    else: print('{username} account is not found, skipped'.format(username=username))

# update data with username given
def update(username):
    is_found_db = is_in_database(username)
    is_found_ig = is_account_found(username)
    # is account is not in database and found add to table
    if not is_found_db and is_found_ig:
        print('new username! inserted to db')
        insert_to_influencer_db(username=username)
    # update data with username given
    main(username=username)

# synchronize data 
def sync():
    query_select = 'SELECT * FROM influencer_username'
    cursor.execute(query_select)
    data = cursor.fetchall()
    influencer_list = [influencer['username'] for influencer in data]
    for influencer in influencer_list:
        main(username=influencer)
    print('data is updated!')