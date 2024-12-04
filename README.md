# Installation

To install and run the RAG Chatbot, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/IordanisSap/RAG-Chatbot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd RAG-Chatbot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Download and install an embeddings model e.g. [nomic-embed-text](https://ollama.com/library/nomic-embed-text)


5. Download and install an LLM e.g. [LLama3.2](https://ollama.com/library/llama3.2)

6. Modify the [config.yaml](app/chatbot//config.yaml) `model` and `embedding-model` values if needed

7. Start the RAG Chatbot:
Development

    ```bash
    flask --app app run --debug
    ```
Production

    ```bash
    gunicorn --workers=3 -b 0.0.0.0:8000 run:gunicorn_app --daemon
    ```


8. Open your web browser and navigate to `http://localhost:5000` to access the chatbot.
