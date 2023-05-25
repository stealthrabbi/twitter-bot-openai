import logging

from dotenv import load_dotenv

from src.open_ai_requestor import OpenAiRequestor
from src.twitter_bot import TwitterBot
from src.tracery_tweet_message_generator import TraceryTweetMessageGenerator


def _configure_logger() -> None:
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main(request=None):
    _configure_logger()
    logger = logging.getLogger(__name__)
    logger.debug(f"request: {request}")
    load_dotenv()
    logger.info("posting AI tweet")
    post_ai_tweet()
    logger.info("post tracery tweet")
    post_tracery_tweet
    return "Success Tweet function"


def post_ai_tweet():
    logger = logging.getLogger(__name__)
    message_generator = OpenAiRequestor()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_OPEN_AI)

    tweet_text = message_generator.get_random_tweet()

    logger.info(f"posting AI tweet: {tweet_text}")
    twitter_bot.post_tweet(tweet_text)


def post_tracery_tweet():
    logger = logging.getLogger(__name__)
    message_generator = TraceryTweetMessageGenerator()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_TRACERY)

    tweet_text = message_generator.get_random_tweet()

    logger.info(f"posting tracery tweet: {tweet_text}")
    twitter_bot.post_tweet(tweet_text)


if __name__ == "__main__":
    main()
