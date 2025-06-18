# Importing AstraDBVectorStore to store and retrieve vectors from Astra DB
from langchain_astradb import AstraDBVectorStore

# Importing HuggingFace embeddings to convert text into vectors
from langchain_huggingface import HuggingFaceEndpointEmbeddings

# Importing the custom DataConverter class to convert CSV reviews to LangChain Document objects
from flipkart.data_converter import DataConverter

# Importing configuration values like model name and API credentials
from flipkart.config import Config

# Defining a class named DataIngestor to handle embedding and storing documents
class DataIngestor:
    # Constructor method to set up embedding model and vector store
    def __init__(self):
        # Creating an embedding model using Hugging Face with model specified in Config
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        
        # Initializing the AstraDB vector store with embedding and config values
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,                          # Embedding model for vectorization
            collection_name="flipkart",                        # Name of the collection in Astra DB
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,         # API endpoint from config
            token=Config.ASTRA_DB_APPLICATION_TOKEN,           # Auth token from config
            namespace=Config.ASTRA_DB_KEYSPACE                 # Keyspace (database namespace)
        )

    # Method to ingest documents into the vector store
    def ingest(self, load_existing=True):
        # If load_existing is True, skip ingestion and return existing vector store
        if load_existing:
            return self.vstore
        
        # Otherwise, convert the CSV reviews to Document objects
        docs = DataConverter("data/flipkart_product_review.csv").convert()
        
        # Add the converted documents to the vector store
        self.vstore.add_documents(docs)
        
        # Return the vector store object
        return self.vstore
