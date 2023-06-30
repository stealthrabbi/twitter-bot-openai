import os
from datetime import datetime
import logging
import time
from typing import List

import tweepy


logger = logging.getLogger(__name__)

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
        chunks = self._split_text(message)

        logger.info(f"tweet chunks: {chunks}")

        # Post the first tweet
        first_chunk = chunks[0]
        logger.info(f"sending tweet 0 at {datetime.now()}: {first_chunk}")
        tweet = self.client.create_tweet(text=first_chunk)
        reply_to_tweet_id = tweet.data["id"]

        logger.info(f"Created initial tweet. ID: {reply_to_tweet_id}")

        # Post the remaining tweets as replies
        for chunk in chunks[1:]:
            tweet = self.client.create_tweet(
                text=chunk, in_reply_to_tweet_id=reply_to_tweet_id
            )
            logger.info(f"sending chunk tweet at {datetime.now()}: {chunk}")
            reply_to_tweet_id = tweet.data["id"]
            time.sleep(0.1)  # Add a delay between each tweet (in seconds)

    def _split_text(self, text: str, chunk_size=280) -> List[str]:
        """Splits the text in to chunks given the size. Splitting is done on whole words.
        Chunk ends if the next word would put the chunk over the size limit"""
        words = text.split()
        chunks = []
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= chunk_size:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
