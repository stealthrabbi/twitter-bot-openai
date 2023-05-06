import os
from datetime import datetime


import tweepy

# see https://docs.tweepy.org/en/stable/examples.html


class TwitterBot:
    AUTH_KEY_SET_TRACERY = "tracery"
    AUTH_KEY_SET_OPEN_AI = "open-ai"

    """ Handles authentication and sending of tweets"""

    def __init__(self, auth_key_set: str):
        if auth_key_set == "tracery":
            access_token = os.getenv("tracery_bot_access_token")
            access_token_secret = os.getenv("tracery_bot_access_token_secret")

            # AKA consumer key/secret
            consumer_key = os.getenv("tracery_bot_consumer_key")
            consumer_secret = os.getenv("tracery_bot_consumer_secret")

            bearer_token = os.getenv("tracery_bot_bearer_token")

        else:
            access_token = os.getenv("open_ai_bot_access_token")
            access_token_secret = os.getenv("open_ai_bot_access_token_secret")

            # AKA consumer key/secret
            consumer_key = os.getenv("open_ai_bot_consumer_key")
            consumer_secret = os.getenv("open_ai_bot_consumer_secret")

            bearer_token = os.getenv("open_ai_bot_bearer_token")

        self.client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token,
        )
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        self.api = tweepy.API(auth)

    def post_tweet(self, message: str):
        if os.getenv("SEND_TWEETS").lower() == "true":
            print(f"sending tweet at {datetime.now()}: {message}")
            self.client.create_tweet(text=message)
        else:
            print(f"simulated tweet: {message}")
