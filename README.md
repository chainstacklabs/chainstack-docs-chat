# Chainctack docs chat bot

MVP for docs specific chat bot.

## Requirements

Before getting started, ensure you have the following:

* [Python](https://www.python.org/downloads/) - Version 3.7 or newer is required.
* An active account on OpenAI, along with an [OpenAI API key](https://platform.openai.com/account/api-keys).
* A Deep Lake account, complete with a [Deep Lake API key](https://app.activeloop.ai/?utm_source=referral&utm_medium=platform&utm_campaign=signup_promo_settings&utm_id=plg).

## Quickstart

- Clone the repository

- Create new Python virtual environment

- Get into the project's directory

```sh
cd chainstack-docs-chat
```

- Install dependencies

```sh
pip install -r requirements.txt
```

- Add API keys to `.env`

```env
# OpenAI 
OPENAI_API_KEY=""
EMBEDDINGS_MODEL="text-embedding-ada-002"
LANGUAGE_MODEL="gpt-3.5-turbo" # gpt-4 gpt-3.5-turbo

# Deeplake vector DB
ACTIVELOOP_TOKEN=""
DATASET_PATH="./local_vector_db" # "hub://USER_ID/custom_dataset"  # Edit with your user id if you want to use the cloud db.

# Scrape settings
SITE_MAP="https://docs.chainstack.com/sitemap.xml"
```

- Run main file to index the docs

```sh
python3 main.py
```

It should be indexing arount 400 pages, it should take about 2 minutes.

- Run the chat script

```sh
Pyrhon3 chat.py
```


 
