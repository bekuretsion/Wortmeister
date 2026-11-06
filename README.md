# WortMeister

A German vocabulary trainer with daily review, flashcards, quizzes, listening, pronunciation practice, and linked words and expressions.

[Open WortMeister](https://bekuretsion.github.io/Wortmeister/)

## Project structure

```text
app/              Application code and collection interfaces
static/css/       Stylesheets
seeds/            Vocabulary data and browser datasets
docs/             Development notes and import audits
tests/            Application and vocabulary checks
tools/            Local server, publishing, extraction, and build tools
index.html        Website entry point
```

Run locally with `node tools/server.cjs`, then open http://127.0.0.1:8765.

Run checks with `node --test tests/core.test.cjs tests/book.test.cjs tests/dictionary.test.cjs`.

Prepare the static website with `node tools/prepare-publish.cjs`. GitHub Pages serves the repository root. Keep `index.html`, `app/`, `seeds/`, and `static/` at their relative paths when deploying.

See [development notes](docs/DEVELOPMENT.md) for maintenance commands.
