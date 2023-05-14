from functools import wraps
from http import HTTPStatus
import os
import logging
from datetime import datetime
import sys

from dotenv import load_dotenv


from flask import Flask, Request, request, Response
from flask import Flask
from src.open_ai_requestor import OpenAiRequestor
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.twitter_bot import TwitterBot
from src.tracery_tweet_message_generator import TraceryTweetMessageGenerator

logger: logging.Logger

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

# if running locally, the env can't be read yet.
tweet_limit = os.getenv("TWEET_LIMIT") or "1 per hour"
print(tweet_limit)


def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_response = check_authorization(request)
        if auth_response.status_code != HTTPStatus.ACCEPTED:
            return auth_response
        return f(*args, **kwargs)

    return decorated


def check_authorization(request: Request) -> Response:
    if request and request.authorization:
        expected_username = os.getenv("AUTH_USER")
        expected_password = os.getenv("AUTH_PASSWORD")

        username = request.authorization.username
        password = request.authorization.password
        logging.info(f"login requested for {username}")
        if username == expected_username and password == expected_password:
            return Response("logged in", status=HTTPStatus.ACCEPTED)
        return Response("bad login", status=HTTPStatus.UNAUTHORIZED)
    return Response("forbidden!!", status=HTTPStatus.FORBIDDEN)


@app.route("/")
def home():
    return "Service Online!! (from root)"


@app.route("/api/health")
@limiter.limit("2 per minute")
def health_check():
    _get_logger().debug("in healthcheck()")
    return "Service Online!!"


@app.route("/api/auth-check")
@require_authentication
def auth_check():
    _get_logger().debug("in authcheck")
    return check_authorization(request)


@app.route("/api/post-tracery-tweet")
@require_authentication
@limiter.limit(tweet_limit)
def post_tracery_tweet():
    _get_logger().info("in post-tracery-tweet")

    message_generator = TraceryTweetMessageGenerator()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_TRACERY)

    tweet_text = message_generator.get_random_tweet()
    twitter_bot.post_tweet(tweet_text)

    return "Tracery Tweet Sent"


@app.route("/api/post-openai-tweet")
@require_authentication
@limiter.limit(tweet_limit)
def post_openai_tweet():
    _get_logger().info("in post-openai-tweet")

    message_generator = OpenAiRequestor()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_OPEN_AI)

    tweet_text = message_generator.get_random_tweet()

    twitter_bot.post_tweet(tweet_text)

    return "OpenAI Tweet Sent"


def start_flask_server():
    _get_logger().debug("starting flask")
    app.run()
    _get_logger().debug("flask ended")


def main():
    _configure_logger()
    load_dotenv()
    start_flask_server()


def _configure_logger() -> None:
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Create a file handler
    os.makedirs("logs", exist_ok=True)
    file_name = f"./logs/app{str(datetime.now().date())}.log"
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the root logger
    logger = logging.getLogger()
    logger.addHandler(file_handler)


def _get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    return logger


if __name__ == "__main__":
    main()
