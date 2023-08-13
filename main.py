import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import DeepLake
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback


def remove_nav_and_header_elements(content: BeautifulSoup) -> str:
    # Remove navigation and header elements from HTML content
    nav_elements = content.find_all('nav')
    header_elements = content.find_all('header')
    for element in nav_elements + header_elements:
        element.decompose()
    return str(content.get_text())


def load_configuration():
    # Load environment variables from .env file
    load_dotenv()
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ACTIVELOOP_TOKEN': os.getenv('ACTIVELOOP_TOKEN'),
        'SITE_MAP': os.getenv('SITE_MAP'),
        'DATASET_PATH': os.getenv('DATASET_PATH'),
        'LANGUAGE_MODEL': os.getenv('LANGUAGE_MODEL')
    }


def load_documents(config):
    # Load pages from Chainstack sitemap using SitemapLoader
    print('Load pages from Chainstack sitemap...')
    loader = SitemapLoader(
        config['SITE_MAP'],
        filter_urls=["https://docs.chainstack.com/docs/", "https://docs.chainstack.com/reference/"],
        parsing_function=remove_nav_and_header_elements
    )
    return loader.load()


def split_documents(documents):
    # Split documents into chunks using TokenTextSplitter
    """
    Check https://blog.davideai.dev/the-ultimate-langchain-series-text-splitters?source=more_series_bottom_blogs#heading-chunk-size-and-overlap
    to understand more about the splitter
    """

    # Extract metadata from the documents if you want to use it for something
    metadatas = [doc.metadata for doc in documents]

    print("=" * 100)
    print('Splitting documents...')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    text = text_splitter.split_documents(documents)
    print(f'Generated {len(text)} chunks.')
    return text


def create_vector_db(text, config):
    # Create and update a vector database using DeepLake
    print("=" * 100)
    print('Creating vector DB...')
    embeddings = OpenAIEmbeddings(disallowed_special=())
    deeplake_path = config['DATASET_PATH']
    db = DeepLake(dataset_path=deeplake_path, embedding_function=embeddings, overwrite=True)
    db.add_documents(text)
    print('Vector database updated.')
    return db


def initialize_retriever(db):
    # Initialize retriever with specific search parameters
    """
    Check https://blog.davideai.dev/the-ultimate-langchain-series-chat-with-your-data#heading-setting-up-the-retriever 
    to understand more about the retriver
    """
    retriever = db.as_retriever()
    retriever.search_kwargs.update({
        'distance_metric': 'cos',
        'fetch_k': 100,
        'maximal_marginal_relevance': True,
        'k': 10,
    })
    return retriever


def main():
    # Main execution flow
    config = load_configuration()
    os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
    os.environ['ACTIVELOOP_TOKEN'] = config['ACTIVELOOP_TOKEN']

    documents = load_documents(config)
    text = split_documents(documents)
    db = create_vector_db(text, config)
    retriever = initialize_retriever(db)

    language_model = config['LANGUAGE_MODEL']
    model = ChatOpenAI(model_name=language_model, temperature=0)
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever, return_source_documents=True)

    # Iterate through questions and print answers. This is to test the indexing process was successful
    questions = [
        "What are the Chainstack's core pillars?",
        "Does Chainstack have a guide on eth_getBlockReceipts?"
    ]
    chat_history = []
    for question in questions:
        with get_openai_callback() as tokens_usage:
            result = qa({"question": question, "chat_history": chat_history})
            chat_history.append((question, result['answer']))   

            first_document = result['source_documents'][0]
            metadata = first_document.metadata
            source = metadata['source']

            print(f"-> **Question**: {question}\n")
            print(f"**Answer**: {result['answer']}\n")
            print(f"++source++: {source}")
            print(tokens_usage)


if __name__ == "__main__":
    main()
