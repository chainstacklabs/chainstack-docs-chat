import os
from dotenv import load_dotenv
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def load_environment_variables():
    """Load environment variables from .env file."""
    load_dotenv()
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN')

def initialize_embeddings():
    """Initialize OpenAI embeddings and disallow special tokens."""
    return OpenAIEmbeddings(disallowed_special=())

def initialize_deeplake(embeddings):
    """Initialize DeepLake vector store with OpenAI embeddings."""
    return DeepLake(
        dataset_path=os.getenv('DATASET_PATH'),
        read_only=True,
        embedding=embeddings,
    )

def initialize_retriever(deep_lake):
    """Initialize retriever and set search parameters."""
    retriever = deep_lake.as_retriever()
    retriever.search_kwargs.update({
        'distance_metric': 'cos',
        'fetch_k': 100,
        'maximal_marginal_relevance': True,
        'k': 10,
    })
    return retriever

def initialize_chat_model():
    """Initialize ChatOpenAI model."""
    return ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], model_name=os.getenv('LANGUAGE_MODEL'), temperature=0.0)

def initialize_conversational_chain(model, retriever):
    """Initialize ConversationalRetrievalChain."""
    return ConversationalRetrievalChain.from_llm(model, retriever=retriever, return_source_documents=True)

def get_user_input():
    """Get user input and handle 'quit' command."""
    question = input("\nPlease enter your question (or 'quit' to stop): ")
    return None if question.lower() == 'quit' else question

# In case you want to format the result.
def print_answer(question, answer):
    """Format and print question and answer."""
    print(f"\nQuestion: {question}\nAnswer: {answer}\n")

def main():
    """Main program loop."""
    load_environment_variables()
    embeddings = initialize_embeddings()
    deep_lake = initialize_deeplake(embeddings)
    retriever = initialize_retriever(deep_lake)
    model = initialize_chat_model()
    qa = initialize_conversational_chain(model, retriever)

    # In this case the chat history is stored in memory only
    chat_history = []

    while True:
        question = get_user_input()
        if question is None:  # User has quit
            break
        
        # Get results based on question
        result = qa({"question": question, "chat_history": chat_history})
        chat_history.append((question, result['answer']))   

        # Take the first source to display
        first_document = result['source_documents'][0]
        metadata = first_document.metadata
        source = metadata['source']

        # We are streaming the response so no need to print those
        #print(f"-> **Question**: {question}\n")
        #print(f"**Answer**: {result['answer']}\n")
        print(f"\n\n++source++: {source}")

if __name__ == "__main__":
    main()
