from dotenv import load_dotenv


from src.open_ai_requestor import OpenAiRequestor
from src.twitter_bot import TwitterBot
from src.tracery_tweet_message_generator import TraceryTweetMessageGenerator


def main():
    print("loading dotenv")
    load_dotenv()
    print("posting AI tweet")
    post_ai_tweet()
    print("post tracery tweet")
    post_tracery_tweet


def post_ai_tweet():
    message_generator = OpenAiRequestor()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_OPEN_AI)

    tweet_text = message_generator.get_random_tweet()

    print(f"posting {tweet_text}")
    twitter_bot.post_tweet(tweet_text)


def post_tracery_tweet():
    message_generator = TraceryTweetMessageGenerator()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_TRACERY)

    tweet_text = message_generator.get_random_tweet()
    twitter_bot.post_tweet(tweet_text)


if __name__ == "__main__":
    main()
