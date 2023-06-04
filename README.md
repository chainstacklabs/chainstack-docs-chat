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

## Example interaction

Sample interaction using the GPT3.5-turbo model. Use GPT4 for better responses.

```
Please enter your question (or 'quit' to stop): what are chainstack core pillars?

Question: what are chainstack core pillars?
Answer: Chainstack's core pillars are unbeatable pricing, unbounded performance, and unlimited flexibility.

Tokens Used: 1178
        Prompt Tokens: 1160
        Completion Tokens: 18
Successful Requests: 1
Total Cost (USD): $0.002356

Please enter your question (or 'quit' to stop): how can i start using the Ethereum API with chainstack?

Question: how can i start using the Ethereum API with chainstack?
Answer: To use the Ethereum API with Chainstack, you need to follow these steps:

1. Sign up with Chainstack.
2. Deploy an Ethereum RPC node.
3. View your node access and credentials.
4. Create an API key to authenticate your requests to the Chainstack API.
5. Use tools such as curl or Postman to make manual requests to the Ethereum RPC node using JSON-RPC and the command line.

Once you have completed these steps, you can start using the Ethereum API to interact with the Ethereum blockchain and build your applications.

Tokens Used: 1389
        Prompt Tokens: 1266
        Completion Tokens: 123
Successful Requests: 2
Total Cost (USD): $0.0027780000000000005

Please enter your question (or 'quit' to stop): what methods can i use to get ethereum blocks information?

Question: what methods can i use to get ethereum blocks information?
Answer: The following methods can be used to retrieve Ethereum block information when using the Ethereum API with Chainstack:

- eth_blockNumber
- eth_getBlockByHash
- eth_getBlockByNumber
- eth_getBlockTransactionCountByHash
- eth_getBlockTransactionCountByNumber
- eth_newBlockFilter

These methods allow developers to access specific block details such as the block's transactions, timestamp, height, header, and more.

Tokens Used: 1846
        Prompt Tokens: 1739
        Completion Tokens: 107
Successful Requests: 2
Total Cost (USD): $0.0036920000000000004
```

 
