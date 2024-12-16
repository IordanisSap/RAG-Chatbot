from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort
from .chatbot.chat import process_message, get_llm_name

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/SemanticRAG')
def SemanticRAG():
    return render_template('SemanticRAG.html')

@main.route('/SemanticRAG/conversation', methods=['POST'])
def conversation():
    messages = request.json.get('messages')
    print(messages)
    return render_template('components/conversation.html', messages=messages)

@main.route('/SemanticRAG/passages', methods=['POST'])
def relevant_studies():
    relevant = request.json.get('passages')
    print(relevant)
    return render_template('components/relevant_text.html', passages=relevant)

    

@main.route('/SemanticRAG/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    bot_response = await process_message(user_message)
    bot_name = get_llm_name()
    return jsonify({'response': bot_response, 'name': bot_name})


UPLOAD_FOLDER = "/mnt/10TB/iordanissapidis/datasets/large"

@main.route('/SemanticRAG/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Ensure the file exists in the folder
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        # Return a 404 if the file does not exist
        abort(404)