# Importing necessary Flask functions
from flask import Flask, render_template, request, Response  # 🟨 Added Response for /metrics endpoint

# Importing Prometheus monitoring tools 🟨
from prometheus_client import Counter, generate_latest  # 🟨 Added Prometheus imports

# Importing custom classes for data ingestion and RAG chain creation
from flipkart.data_ingestion import DataIngestor
from flipkart.rag_chain import RAGChainBuilder

# Importing dotenv to load environment variables from .env file
from dotenv import load_dotenv

# Load environment variables from the .env file (e.g., API keys, tokens)
load_dotenv()

# 🟨 Prometheus metrics counter for total HTTP requests
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")  # 🟨

# Function to create and configure the Flask app
def create_app():
    # Initialize a Flask web application
    app = Flask(__name__)

    # Load vector store (from Astra DB) using the DataIngestor class
    # Set load_existing=True to skip re-uploading if already ingested
    vector_store = DataIngestor().ingest(load_existing=True)

    # Build the Retrieval-Augmented Generation (RAG) chain using the vector store
    rag_chain = RAGChainBuilder(vector_store).build_chain()

    # Define a route for the homepage (renders index.html)
    @app.route("/")
    def index():
        REQUEST_COUNT.inc()  # 🟨 Increment Prometheus counter
        return render_template("index.html")  # Load the UI page

    # Define a POST route to handle chatbot user input and return model response
    @app.route("/get", methods=["POST"])
    def get_response():
        REQUEST_COUNT.inc()  # 🟨 Increment Prometheus counter
        # Get the user's message from the form input
        user_input = request.form["msg"]

        # Pass the input to the RAG chain and get the generated answer
        response = rag_chain.invoke(
            {"input": user_input},  # User's question
            config={"configurable": {"session_id": "user-session"}}  # Session ID for chat history
        )["answer"]  # Extract the "answer" field from the output

        return response  # Send the answer back to the frontend

    # 🟨 Prometheus metrics endpoint
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain")  # 🟨

    # Return the Flask app object
    return app


# If this script is run directly (not imported), start the web server
if __name__ == "__main__":
    app = create_app()  # Create the Flask app
    app.run(host="0.0.0.0", port=5000, debug=False)  # Run the app on port 5000, accessible on all IPs
