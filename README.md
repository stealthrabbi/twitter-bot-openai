# twitter-bot-openai

Twitter bot python webapp using OpenAI, tracery

## Development

Poetry can be used to manage dependencies locally. Poetry dependencies must be exported (synchronized) to `requirements.txt` if deploying to Azure app service for python applications,
as by default at least, it installs dependencies from requirements.txt when building the container.

To update requirements.txt, run

```sh
poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt
```
