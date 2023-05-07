import logging
import os
import ast
import random
from typing import List

from dotenv import load_dotenv
import openai

logger = logging.getLogger(__name__)


class OpenAiRequestor:
    # see https://platform.openai.com/docs/models/gpt-3-5
    OPEN_AI_MODEL = "text-davinci-003"
    OPEN_AI_CHAT_MODEL = "gpt-3.5-turbo"

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.open_ai_system_prompt = os.getenv("OPEN_AI_SYSTEM_PROMPT")
        self.open_ai_user_prompt = os.getenv("OPEN_AI_USER_PROMPT_ARRAY")

    # conversation with gpt-3.5-turbo gives more thought out responses than using text-davinci
    def get_random_tweet(self) -> str:
        logger.debug("getting chat response")
        user_prompt = self._get_random_ai_user_prompt()
        response = openai.ChatCompletion.create(
            model=self.OPEN_AI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": self.open_ai_system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        logger.debug(response)
        response_text = response["choices"][0]["message"]["content"]

        logger.info(f"response text: {response_text}")
        logger.info(f"Number of tokens: {response['usage']['total_tokens']}")
        return response_text

    def _get_random_ai_user_prompt(self) -> str:
        # Convert the input string to a list of strings using ast.literal_eval

        random_prompt = self.open_ai_user_prompt
        try:
            user_prompts_array: List[str] = ast.literal_eval(self.open_ai_user_prompt)

            random_prompt = random.choice(user_prompts_array)
        except (SyntaxError, ValueError) as e:
            logger.warning("Error evaluating user prompt array")
        logger.info(f"Using prompt: {random_prompt}")
        return random_prompt


if __name__ == "__main__":
    load_dotenv()
    requestor = OpenAiRequestor()
    requestor.get_random_tweet()
