from http import HTTPStatus
import os


from dotenv import load_dotenv


from flask import Flask, Request, request, Response
from flask import Flask
from src.open_ai_requestor import OpenAiRequestor

from src.twitter_bot import TwitterBot
from src.tracery_tweet_message_generator import TraceryTweetMessageGenerator

app = Flask("")


def _check_authorization(request: Request) -> Response:
    if request and request.authorization:
        expected_username = os.getenv("AUTH_USER")
        expected_password = os.getenv("AUTH_PASSWORD")

        username = request.authorization.username
        password = request.authorization.password
        print(f"login requested for {username}")
        if username == expected_username and password == expected_password:
            return Response("logged in", status=HTTPStatus.ACCEPTED)
        return Response("bad login", status=HTTPStatus.UNAUTHORIZED)
    return Response("forbidden!!", status=HTTPStatus.FORBIDDEN)


@app.route("/")
def home():
    print("in home()")
    return "Service Online!! (from root)"


@app.route("/api/health")
def health_check():
    print("in healthcheck()")
    return "Service Online!!"


@app.route("/api/auth-check")
def auth_check():
    print("in authcheck")
    return _check_authorization(request)


@app.route("/api/post-tracery-tweet")
def post_tracery_tweet():
    print("in post-tracery-tweet")
    authorization_response = _check_authorization(request)
    if authorization_response.status_code != HTTPStatus.ACCEPTED:
        return authorization_response

    message_generator = TraceryTweetMessageGenerator()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_TRACERY)

    tweet_text = message_generator.get_random_tweet()
    twitter_bot.post_tweet(tweet_text)

    return "Tracery Tweet Sent"


@app.route("/api/post-openai-tweet")
def post_openai_tweet():
    print("in post-tracery-tweet")
    authorization_response = _check_authorization(request)
    if authorization_response.status_code != HTTPStatus.ACCEPTED:
        return authorization_response

    message_generator = OpenAiRequestor()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_OPEN_AI)

    tweet_text = message_generator.get_random_tweet()

    twitter_bot.post_tweet(tweet_text)

    return "OpenAI Tweet Sent"


def start_flask_server():
    print("starting flask")
    app.run()
    print("flask ended")


def main():
    load_dotenv()
    start_flask_server()


if __name__ == "__main__":
    main()
