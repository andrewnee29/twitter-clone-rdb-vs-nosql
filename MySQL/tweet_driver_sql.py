from tweet_mysql import TwitterAPI
from tweet_objects import Tweet, Follower
import pandas as pd
import time
import os

def main():

    # Authenticate
    api = TwitterAPI(os.environ["username"], os.environ["password"], "twitter")

    # Read your CSVs
    tweet_df = pd.read_csv("tweet.csv")
    follows_df = pd.read_csv("follows.csv")

    # Insert follows row by row
    for index, row in follows_df.iterrows():
        follower = Follower(int(row['USER_ID']), int(row['FOLLOWS_ID']))  # Use column names
        api.follow_user(follower)

    """
    My computer wasn't able to insert all 1 million tweets into the database.
    I'm going to compute it by hand, but the following post_tweet code is how I would do it
    if my computer were able to insert all of the rows.
    """
    # Insert tweets row by row and measure performance
    start_time = time.time()
    call_count = 0

    # Insert tweets row by row
    for index, row in tweet_df.iterrows():
        tweet = Tweet(row['USER_ID'], row['TWEET_TEXT'])  # Use column names
        api.post_tweet(tweet)
        call_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    calls_per_second = call_count / elapsed_time

    print(f"Made {call_count} calls in {elapsed_time:.2f} seconds")
    print(f"Tweets per second: {calls_per_second:.2f}")

    # Timing get_home_timeline
    start_time = time.time()
    call_count = 0

    for i in range(100):  # Make 100 calls
        random_user_id = api.get_random_user()
        random_user_id = random_user_id.iloc[0, 0]

        timeline = api.get_home_timeline(random_user_id)
        timeline_tweets = [Tweet(int(row['followee_id']), row['tweet_text'])  # list of tweet objects
                           for index, row in timeline.iterrows()]
        call_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    calls_per_second = call_count / elapsed_time

    print(f"Made {call_count} calls in {elapsed_time:.2f} seconds")
    print(f"Calls per second: {calls_per_second:.2f}")

if __name__ == '__main__':
    main()