import os
import logging
from datetime import datetime

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

from src.open_ai_requestor import OpenAiRequestor

from src.twitter_bot import TwitterBot
from src.tracery_tweet_message_generator import TraceryTweetMessageGenerator

logger: logging.Logger

app = FastAPI()
security = HTTPBasic()


def _configure_logger() -> None:
    print("configuring logger now")
    # Configure the root logger
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # )

    # Create a file handler
    os.makedirs("logs", exist_ok=True)
    file_name = f"./logs/app-{str(datetime.now().date())}.log"
    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add the handlers to the root logger
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)


_configure_logger()


def get_authenticated_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    expected_username = os.getenv("AUTH_USER")
    expected_password = os.getenv("AUTH_PASSWORD")

    # Perform authentication logic here, e.g., check against a database or external service
    logging.info(f"login requested for {username}")
    if username == expected_username and password == expected_password:
        return username

    raise HTTPException(status_code=401, detail="Unauthorized!")


@app.head("/")
async def home():
    return "Service Online!! (from root)"


@app.head("/api/health")
async def health_check(request: Request) -> str:
    logger.info("Health check")
    return "Service Online!!"


@app.head("/api/auth-check")
async def auth_check(user=Depends(get_authenticated_user)):
    logger().debug("in authcheck")


@app.head("/api/post-tracery-tweet")
async def post_tracery_tweet(user=Depends(get_authenticated_user)):
    logger().info("in post-tracery-tweet")

    message_generator = TraceryTweetMessageGenerator()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_TRACERY)

    tweet_text = message_generator.get_random_tweet()
    twitter_bot.post_tweet(tweet_text)

    return "Tracery Tweet Sent"


@app.head("/api/post-openai-tweet")
async def post_openai_tweet(user=Depends(get_authenticated_user)):
    logger().info("in post-openai-tweet")

    message_generator = OpenAiRequestor()
    twitter_bot = TwitterBot(TwitterBot.AUTH_KEY_SET_OPEN_AI)

    tweet_text = message_generator.get_random_tweet()

    twitter_bot.post_tweet(tweet_text)

    return "OpenAI Tweet Sent"


def start_web_server():
    logger.debug("starting webapp")
    uvicorn.run("app:app", host="0.0.0.0")
    logger.debug("webapp ended")


def main():
    load_dotenv()
    start_web_server()


def _get_logger() -> logging.Logger:
    return logger


if __name__ == "__main__":
    main()
