# Installation

To install and run the RAG Chatbot, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/RAG-Chatbot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd RAG-Chatbot
    ```

3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - For Windows:

      ```bash
      venv\Scripts\activate
      ```

    - For macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Download and install an embeddings model e.g. [nomic-embed-text](https://ollama.com/library/nomic-embed-text)


7. Download and install an LLM e.g. [LLama3.2](https://ollama.com/library/llama3.2)

8. Modify the [config.yaml](app/chatbot//config.yaml) `model` and `embedding-model` values if needed

9. Start the RAG Chatbot:

    ```bash
    flask --app app run --debug
    ```

10. Open your web browser and navigate to `http://localhost:5000` to access the chatbot.
