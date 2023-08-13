# Chainctack docs chat bot

Simple CLI implemenation of a docs specific AI assistant. This project guides you to build an AI assistant for the Chainstack documentation using LangChain and Activeloop.

Read the article for an in depth guide:

- [LangChain practical projects — build a CLI chatbot](https://blog.davideai.dev/langchain-practical-projects-build-a-cli-chatbot)

## Requirements

Before getting started, ensure you have the following:

- [Python](https://www.python.org/downloads/) - Version 3.7 or newer is required.
- An active account on OpenAI, along with an [OpenAI API key](https://platform.openai.com/account/api-keys).
- An Activeloop account, complete with a [Activeloop API key](https://app.activeloop.ai/?utm_source=referral&utm_medium=platform&utm_campaign=signup_promo_settings&utm_id=plg).

## Project structure

- `.env` stores secrets and configuration as environment variables.
- `main.py` scrapes pages and creates vector database.
- `chat.py` accepts users queries.

## Quickstart

- Clone the repository

```sh
git clone https://github.com/soos3d/chainstack-docs-chat.git
```

- Get into the project's directory

```sh
cd chainstack-docs-chat
```

- Create new Python virtual environment

```sh
python3 -m venv docs-chat
```

- Activate the virtual environment:

```sh
source docs-chat/bin/activate
```

- Install dependencies

```sh
pip install -r requirements.txt
```

- Add API keys and config to the `.env` file:

```env
# OpenAI
OPENAI_API_KEY=""
EMBEDDINGS_MODEL="text-embedding-ada-002"
LANGUAGE_MODEL="gpt-3.5-turbo" # gpt-4 gpt-3.5-turbo

# Deeplake vector DB
ACTIVELOOP_TOKEN=""
DATASET_PATH="./chainstack_docs" # "hub://USER_ID/custom_dataset"  # Edit with your user id if you want to use the cloud db.

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
Please enter your question (or 'quit' to stop): What are Chainstack core pillars?
Chainstack's core pillars are:

1. Unbeatable pricing: Chainstack offers competitive pricing options for its services. You can check their pricing options and use the pricing calculator on their website or contact them for more information.

2. Unbounded performance: Chainstack does not impose rate limiting or hard caps on its services. This means that you can enjoy high-performance and scalability without any restrictions.

3. Unlimited flexibility: Chainstack provides unlimited flexibility to its users. You can customize your node settings, such as the txpool.pricebump, and access additional node resources. They also offer load balancing and other customization options to meet your specific needs.

++source++: https://docs.chainstack.com/docs/platform-introduction
```

```
Please enter your question (or 'quit' to stop): How can I start using the Ethereum API with Chainstack?
To start using the Ethereum API with Chainstack, you can follow these steps:

1. Sign up with Chainstack: Visit the Chainstack website and sign up for an account.

2. Deploy a node: Once you have signed up, deploy an Ethereum node on Chainstack. You can choose the network you want to deploy (such as the Ethereum Sepolia testnet) and configure the node according to your needs.

3. View node access and credentials: After deploying the node, you will be able to view the access details and credentials for your node. This includes the RPC URL, which you will need to connect to the network.

4. Connect to the network: Use the RPC URL provided by Chainstack to connect to the Ethereum network. You can use libraries like web3.js to interact with the network and perform various operations such as reading the latest block number or sending transactions.

By following these steps, you will be able to start using the Ethereum API with Chainstack and interact with the Ethereum network.

++source++: https://docs.chainstack.com/docs/ethereum-tutorial-trust-fund-account-with-remix
```

```
Please enter your question (or 'quit' to stop): What methods can I use to get ethereum blocks information?
To get Ethereum blocks information, you can use the following methods:

1. eth_blockNumber: This method returns the number of the most recent block on the Ethereum blockchain.

2. eth_getBlockByHash: This method retrieves a block by its hash.

3. eth_getBlockByNumber: This method retrieves a block by its number.

4. eth_getBlockTransactionCountByHash: This method returns the number of transactions in a block given its hash.

5. eth_getBlockTransactionCountByNumber: This method returns the number of transactions in a block given its number.

6. eth_newBlockFilter: This method creates a new filter that notifies you when a new block is added to the Ethereum blockchain.

These methods allow you to access specific block details such as transactions, timestamp, height, header, and more.

++source++: https://docs.chainstack.com/reference/ethereum-blocks-rpc-methods
```

> Note that this is a basic app and many improvements can be made.
