class Tweet:

    def __init__(self, user_id, tweet_text):
        self.user_id = user_id
        self.tweet_text = tweet_text

class Follower:

    def __init__(self, follower_id, followee_id):
        self.follower_id = follower_id
        self.followee_id = followee_id

    def __str__(self):
        return f"Follower: {self.follower_id} follows {self.followee_id}"

