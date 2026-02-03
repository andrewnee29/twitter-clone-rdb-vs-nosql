from tweet_redis import TwitterAPI
from tweet_objects import Tweet, Follower
import pandas as pd
import time
import os

def main():

    # Activate api
    api = TwitterAPI(host = "localhost", port = 6379)

    # Read your CSVs
    tweet_df = pd.read_csv("tweet.csv")
    follows_df = pd.read_csv("follows.csv")

    # Insert follows row by row
    for index, row in follows_df.iterrows():
        follower = Follower(int(row['USER_ID']), int(row['FOLLOWS_ID']))  # Use column names
        api.follow_user(follower)

    # Insert tweets row by row and measure performance
    start_time = time.time()
    call_count = 0

    # Insert tweets row by row
    for index, row in tweet_df.iterrows():
        tweet = Tweet(row['USER_ID'], row['TWEET_TEXT'])  # Use column names
        tweet_id = api.post_tweet(tweet)
        # print(f"Tweet posted! ID: {tweet_id}")  # Show confirmation to user
        call_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    calls_per_second = call_count / elapsed_time

    print(f"Made {call_count} calls in {elapsed_time:.2f} seconds")
    print(f"Tweets per second: {calls_per_second:.2f}")

    # Timing get_home_timeline
    start_time = time.time()
    call_count = 0

    for i in range(100000):  # Make 100000 calls
        random_user_id = api.get_random_user()
        timeline = api.get_home_timeline(random_user_id)

        # Convert to Tweet objects
        tweet_objects = [
            Tweet(user_id=t['user_id'], tweet_text=t['tweet_text'])
            for t in timeline
        ]
        call_count += 1

    end_time = time.time()
    elapsed_time = end_time - start_time
    calls_per_second = call_count / elapsed_time

    print(f"Made {call_count} calls in {elapsed_time:.2f} seconds")
    print(f"Calls per second: {calls_per_second:.2f}")

if __name__ == '__main__':
    main()