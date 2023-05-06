# twitter-bot-openai

Twitter bot python webapp using OpenAI, tracery

## Development

Poetry can be used to manage dependencies locally. Poetry dependencies must be exported (synchronized) to `requirements.txt` if deploying to Azure app service for python applications,
as by default at least, it installs dependencies from requirements.txt when building the container.

To update requirements.txt, run

```sh
poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt
```

## Open AI - GPT based bot

<< FILL ME IN>>

## Tracery-based bot

This app also supports using [Tracery](http://air.decontextualize.com/tracery/) to generate message and generate tweets as well.
Tracery is a language for generating text based on rules and expansions. Tracery grammars are written in a format called JSON (or “javascript object notation”). JSON is a common format for exchanging data between computer programs written in different programming languages and on different kinds of computers.

Create a file named `tracery.json` to use the tracery bot function. See [tracery.example.json](tracery.example.json) as a template. It is similar to [MadLibs](https://en.wikipedia.org/wiki/Mad_Libs).
