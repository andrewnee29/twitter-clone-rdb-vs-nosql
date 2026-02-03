"""
Tweet-Follow Database API for Redis
"""

import redis
import json

class TwitterAPI:

    def __init__(self, host="localhost", port=6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def post_tweet(self, tweet):

        # assign each tweet an incrementing tweet_id
        tweet_id = self.redis.incr("tweet:id:counter")

        # assign each tweet a key
        tweet_key = f"tweet:{tweet_id}"

        # add tweet as hash
        self.redis.hset(tweet_key, mapping={
            'tweet_id': tweet_id,
            "user_id": tweet.user_id,
            "tweet_text": tweet.tweet_text
        })

        # read followee's followers from set
        followers = self.redis.smembers(f'user:{tweet.user_id}:followers')

        # use sorted sets to hold timelines
        # use the tweet_id as a chronological score
        for follower_id in followers:
            self.redis.zadd(f'user:{follower_id}:timeline', {tweet_id: tweet_id})

        self.redis.sadd('users', tweet.user_id)
        return tweet_id

    def follow_user(self, follower):

        # want a set user:123:followers = {2,45,863}
        self.redis.sadd(f'user:{follower.followee_id}:followers', follower.follower_id)

    def get_home_timeline(self, follower_id):

        # reverse the sorted set as newer tweets are at the end, get top 10
        # get set of tweet_ids
        tweet_ids = self.redis.zrevrange(f'user:{follower_id}:timeline', 0, 9)

        # access hash data with tweet:{tweet_id}
        # append to a list
        timeline = []
        for tweet_id in tweet_ids:
            tweet_data = self.redis.hgetall(f'tweet:{tweet_id}')
            if tweet_data:
                timeline.append(tweet_data)

        return timeline

    def get_random_user(self):
        return self.redis.srandmember('users')
