import tweepy
import time

# Authentication details
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_secret = 'your_access_secret'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# Define the hashtags to search and retweet
hashtags = ['#hashtag1', '#hashtag2', '#hashtag3']

# Define the users to follow back
users_to_follow = []

# Define the time interval between tweets (in seconds)
interval_time = 300

# Define the number of followers/following for which to check unfollowing
unfollow_number = 5000

# Define the main function
def main():
    while True:
        try:
            # Search for tweets with the defined hashtags
            for hashtag in hashtags:
                tweets = tweepy.Cursor(api.search_tweets, hashtag).items(5)
                for tweet in tweets:
                    # Retweet the tweet if it has not been retweeted before
                    if not tweet.retweeted:
                        try:
                            tweet.retweet()
                            print('Retweeted tweet from @' + tweet.author.screen_name)
                            time.sleep(5)
                        except tweepy.TweepError as e:
                            print(e.reason)
            # Follow back the users who follow you
            for follower in tweepy.Cursor(api.followers).items():
                if follower.id not in users_to_follow:
                    follower.follow()
                    print('Followed back @' + follower.screen_name)
                    users_to_follow.append(follower.id)
            # Unfollow users who unfollow you
            for friend in tweepy.Cursor(api.friends).items():
                if friend.followers_count == 0 or friend.followers_count / friend.friends_count < 0.5:
                    api.destroy_friendship(friend.id)
                    print('Unfollowed @' + friend.screen_name)
            # Wait for the defined interval before repeating the loop
            time.sleep(interval_time)
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(10)

if __name__ == '__main__':
    main()
    
