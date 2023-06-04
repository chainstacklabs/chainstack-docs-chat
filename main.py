import os
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
import deeplake

from dotenv import load_dotenv
from bs4 import BeautifulSoup

def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Find all 'nav' and 'header' elements in the BeautifulSoup object
    nav_elements = content.find_all('nav')
    header_elements = content.find_all('header')

    # Remove each 'nav' and 'header' element from the BeautifulSoup object
    for element in nav_elements + header_elements:
        element.decompose()

    # Return the text of the modified BeautifulSoup object
    return str(content.get_text())

def main():
    # Load environment variables from .env file
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')

    site_map = os.getenv('SITE_MAP')
    urls_filter = os.getenv('URLS_FILTER')

    # Config embeddings model
    embeddings = OpenAIEmbeddings(disallowed_special=())

    # Load pages from the sitemap
    loader = SitemapLoader(
        site_map,                                              # Chainstack sitemap
        filter_urls=["https://docs.chainstack.com/docs/", "https://docs.chainstack.com/reference/"], # Only scrape docs pages and refs
        parsing_function=remove_nav_and_header_elements        # Use custom scraping function
    )

    print('Load pages from Chainstack sitemap...')
    documents = loader.load()

    # Split the docs using RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=30)
    print("=" * 100)
    print('Splitting documents...')
    text = text_splitter.split_documents(documents)
    print(f'Generated {len(text)} chunks.')

    # Generate vectors and update the vector db.
    print("=" * 100)
    print('Creating vector DB...')

    # Create a local vector db
    deeplake_path = os.getenv('DATASET_PATH')
    db = DeepLake(dataset_path=deeplake_path, embedding_function=embeddings, overwrite=True)
    db.add_documents(text)
    print('Vector database updated.')

    # Enable the following section and edit the questions to test while indexing a new repository.
"""
    # Initialize DeepLake vector store with OpenAI embeddings
    deep_lake = DeepLake(
        dataset_path=deeplake_path,
        read_only=True,
        embedding_function=embeddings,
    )
    # Initialize retriever and set search parameters
    retriever = deep_lake.as_retriever()
    retriever.search_kwargs.update({
        'distance_metric': 'cos',
        'fetch_k': 100,
        'maximal_marginal_relevance': True,
        'k': 10,
    })

    # List questions to answer in a row.
    # Initialize GPT model
    language_model= os.getenv('LANGUAGE_MODEL')
    model = ChatOpenAI(model_name=language_model, temperature=0.2) # gpt-3.5-turbo by default, edit in .env 
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

    questions = [
        "What are the Chainstack's core pillars:?",
        "What protocols does Chainstack support?",
        "How many Subgraph requests are available on each plan?",
        "Does Chainstack have a guide on eth_getBlockReceipts?"
    ] 
    chat_history = []

    for question in questions:  
        # Display token usage and approximate costs
        with get_openai_callback() as tokens_usage:
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result['answer']))
            print(f"-> **Question**: {question}\n")
            print(f"**Answer**: {result['answer']}\n")
            print(tokens_usage)
"""
if __name__ == "__main__":
    main()