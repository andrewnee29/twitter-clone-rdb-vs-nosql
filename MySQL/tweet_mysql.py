"""
Tweet-Follow Database API for MySQL
"""

from dbutils import DBUtils

class TwitterAPI:

    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def post_tweet(self, tweet):
        sql = "INSERT INTO tweet (user_id, tweet_text) VALUES (%s, %s)"
        val = (tweet.user_id, tweet.tweet_text)
        self.dbu.insert_one(sql, val)

    def follow_user(self, follower):
        sql = "INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s)"
        val = (follower.follower_id, follower.followee_id)
        self.dbu.insert_one(sql, val)

    def get_home_timeline(self, follower_id):
        query = f'''SELECT tweet_text, tweet_ts, followee_id
                     FROM follows LEFT JOIN tweet
                     ON follows.followee_id = tweet.user_id
                     WHERE follows.follower_id = {follower_id}
                     ORDER BY tweet_ts DESC
                     LIMIT 10;'''
        return self.dbu.execute(query)

    def get_random_user(self):
        query = "SELECT user_id FROM tweet ORDER BY RAND() LIMIT 1"
        return self.dbu.execute(query)