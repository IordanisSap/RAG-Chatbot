from flask import Blueprint, render_template, request, jsonify
from .chatbot.chat import process_message

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
    return jsonify({'response': bot_response})