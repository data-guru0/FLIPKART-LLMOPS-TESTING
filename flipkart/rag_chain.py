# Importing ChatGroq LLM for generating responses
from langchain_groq import ChatGroq

# Importing chain builders to create retriever and retrieval chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain

# Importing function to combine documents using "stuff" method for answering
from langchain.chains.combine_documents import create_stuff_documents_chain

# Importing prompt template tools
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Importing runnable that supports chat history
from langchain_core.runnables.history import RunnableWithMessageHistory

# Importing in-memory chat message history
from langchain_community.chat_message_histories import ChatMessageHistory

# Base class for message history
from langchain_core.chat_history import BaseChatMessageHistory

# Importing configuration (contains API keys, model names, etc.)
from flipkart.config import Config

# Class to build a RAG (Retrieval-Augmented Generation) chain
class RAGChainBuilder:
    # Constructor takes the vector store as input
    def __init__(self, vector_store):
        self.vector_store = vector_store  # Save the vector store (retriever)
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature=0.5)  # Load Groq LLM with config model
        self.history_store = {}  # Dictionary to store chat histories per session

    # Private method to get (or create) chat history for a given session ID
    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()  # Create new history if not present
        return self.history_store[session_id]  # Return the stored chat history

    # Method to build the RAG chain
    def build_chain(self):
        # Convert the vector store into a retriever (fetch top 3 relevant docs)
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        # Prompt to rewrite a follow-up question into a standalone question using chat history
        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for past messages
            ("human", "{input}")  # User's current question
        ])

        # Prompt to answer using the context (retrieved docs) and history
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot answering product-related queries using reviews and titles.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"),  # Past conversation
            ("human", "{input}")  # Current user input
        ])

        # Create a retriever that understands conversation history
        history_aware_retriever = create_history_aware_retriever(
            self.model, retriever, context_prompt
        )

        # Create a QA chain that uses the retrieved documents to generate answers
        question_answer_chain = create_stuff_documents_chain(
            self.model, qa_prompt
        )

        # Combine retriever and QA chain into a single retrieval chain
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # Wrap the full chain with message history tracking to support multi-turn chat
        return RunnableWithMessageHistory(
            rag_chain,                       # The RAG chain
            self._get_history,               # Function to get chat history
            input_messages_key="input",      # Key for user input
            history_messages_key="chat_history",  # Key for history input
            output_messages_key="answer"     # Key for model's output
        )
