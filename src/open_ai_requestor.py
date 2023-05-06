

import os
import openai

from dotenv import load_dotenv

class OpenAiRequestor:
    # see https://platform.openai.com/docs/models/gpt-3-5
    OPEN_AI_MODEL="text-davinci-003"
    OPEN_AI_CHAT_MODEL="gpt-3.5-turbo"


    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.open_ai_system_prompt = os.getenv("OPEN_AI_SYSTEM_PROMPT")
        self.open_ai_user_prompt = os.getenv("OPEN_AI_USER_PROMPT")

        

    # conversation with gpt-3.5-turbo gives more thought out responses than using text-davinci
    def get_random_tweet(self) -> str:
        print("getting chat response")
        response = openai.ChatCompletion.create(
            model=self.OPEN_AI_CHAT_MODEL,
            messages=[
                {"role": "system", "content": self.open_ai_system_prompt},
                {"role": "user", "content": self.open_ai_user_prompt}
                ]
            )

        print(response)
        response_text = response["choices"][0]["message"]["content"]

        print(f"response text: {response_text}")
        print(f"Number of tokens: {response['usage']['total_tokens']}")
        return response_text

    def get_random_tweet_old(self) -> str:
        response = openai.Completion.create(
            model=self.OPEN_AI_MODEL,
            prompt=self.OPEN_AI_PROMPT,
            # randomness = Closer to 0 = more deterministic
            temperature=0.7,

            max_tokens=256,
            # diversity in nucleus sampling
            top_p=1,
            # reduces repeition - likely irrelvant for this prompt
            frequency_penalty=0,
            # increases likelihood to talk about new subjects (we don't want this)
            presence_penalty=0
        )

        response_text = response["choices"][0]["text"]

        print(f"response text: {response_text}")
        print(f"Number of tokens: {response['usage']['total_tokens']}")
        return response_text
    
if __name__ == "__main__":
    load_dotenv()
    requestor = OpenAiRequestor()
    requestor.get_random_tweet()