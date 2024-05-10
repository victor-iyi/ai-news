# AI News

Get your latest news on AI and interract with an assitant to give you the
information you need or searching for.

## Setup

### Create virtualenv

Create your virtualenv with built-in `venv` package.

```python
python -m venv .venv
```

Activate your environment.

```sh
source .venv/bin/activate
```

### Install dependencies

Install dependencies using `poetry`.

```sh
poetry install
poetry install --with dev  # for dev
```

### API Keys and Secrets

You have two options to create your API keys: using `.env` file or `streamlit`'s
secrets. Note that you can only use `streamlit` when running the `streamlit` app
locally or when deployed. However, `.env` is advised for local development.

- **Create your secrets with `.env`**

```sh
mv .env.example .env
```

Edit `.env` file.

```sh
OPENAI_API_KEY=sk-...
NEWS_API_KEY=9c...
```

- **Create your secrets & config with `streamlit`**

```sh
mkdir -p ./.streamlit/
touch ./.streamlit/secrets.toml  # for secret keys
touch ./.streamlit/config.toml   # for streamlit config
```

Edit `$CWD/.streamlit/secrets.toml` file.

```toml
OPENAI_API_KEY = "<get API key from platform.openai.com/api-keys>"
NEWS_API_KEY = "<get API key from https://newsapi.org/register>"
```

## Usage

Start your `streamlit` application:

```sh
streamlit run home.py
```

## Contribution

You are very welcome to modify and use them in your own projects.

Please keep a link to the [original repository]. If you have made a fork with
substantial modifications that you feel may be useful, then please
[open a new issue on GitHub][issues] with a link and short description.

## License (MIT)

This project is opened under the [MIT][license] which allows very broad use for
both private and commercial purposes.

A few of the images used for demonstration purposes may be under copyright.
These images are included under the "fair usage" laws.

[original repository]: https://github.com/victor-iyi/ai-news
[issues]: https://github.com/victor-iyi/ai-news/issues
[license]: ./LICENSE
