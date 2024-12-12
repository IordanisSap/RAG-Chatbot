from flask import Blueprint, render_template, request, jsonify
from .chatbot.chat import process_message, get_llm_name

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/SemanticRAG')
def SemanticRAG():
    return render_template('SemanticRAG.html')

@main.route('/SemanticRAG/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    bot_response = await process_message(user_message)
    bot_name = get_llm_name()
    return jsonify({'response': bot_response, 'name': bot_name})