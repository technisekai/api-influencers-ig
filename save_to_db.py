from connect_db import *

# insert data to `basic_information_account` table
def insert_to_basic_db(data):
    select_query = 'SELECT * FROM basic_information_account WHERE date_scrap="{date_scrap}" AND username="{username}"'.format(date_scrap=data['date_scrap'], username=data['username'])
    is_in_db = cursor.execute(select_query)
    if is_in_db:
        update_query = 'UPDATE basic_information_account SET followers="{followers}", following="{following}", total_posts="{total_posts}", total_likes="{total_likes}", total_comments="{total_comments}", engagment_rate="{engagment_rate}" WHERE date_scrap="{date_scrap}" AND username="{username}"'.format(followers=data['followers'], following=data['following'], total_posts=data['total_posts'], total_likes=data['total_likes'], total_comments=data['total_comments'], engagment_rate=data['engagment_rate'], date_scrap=data['date_scrap'], username=data['username'])
        cursor.execute(update_query)
        connection.commit()
    else:
        values = ', '.join(['"{value}"'.format(value=i) for i in data.values()])
        insert_query = "INSERT INTO `basic_information_account` VALUES({values});".format(values=values)
        cursor.execute(insert_query)
        connection.commit()

# insert data to `posts_information_account` table
def insert_to_post_db(data):
    for x in data:
        select_query = 'SELECT * FROM posts_information_account WHERE shortcode="{shortcode}";'.format(shortcode=x['shortcode'][:-3])
        shortcode_in_db = cursor.execute(select_query)
        if shortcode_in_db:
            update_query = 'UPDATE posts_information_account SET date_scrap="{date_scrap}", caption="{caption}", count_likes="{count_likes}", count_comments="{count_comments}" WHERE shortcode="{shortcode}";'.format(date_scrap=x['date_scrap'], caption=x['caption'], count_likes=x['count_likes'], count_comments=x['count_comments'], shortcode=x['shortcode'][:-3])
            cursor.execute(update_query)
            connection.commit()
        else:
            values = ', '.join(['"{value}"'.format(value=i) for i in x.values()])
            query = "INSERT INTO `posts_information_account` VALUES({values});".format(values=values)
            cursor.execute(query)
            connection.commit()

# check if username in `influencer_username` table
def is_in_database(username):
    select_query = 'SELECT * FROM influencer_username WHERE username="{username}";'.format(username=username)
    cursor.execute(select_query)
    is_found = cursor.fetchone()
    return is_found

# insert new username to `influencer_username` table
def insert_to_influencer_db(username):
    insert_query = 'INSERT INTO `influencer_username` VALUES("{username}");'.format(username=username)
    cursor.execute(insert_query)
    connection.commit()