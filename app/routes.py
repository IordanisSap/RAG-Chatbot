from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort, redirect, url_for
from .chatbot.chat import process_message, get_llm_name, search_query

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect("/SemanticRAG")

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
    query = request.json.get('query')
    return render_template('components/search_results.html', documents=relevant, keywords=query.split(' '))

    

@main.route('/SemanticRAG/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    
    try: 
        topk = int(request.args.get('topk'))
        score_threshold = float(request.args.get('score_threshold'))
        if topk <= 0 or score_threshold <= 0 : raise ValueError("topk value must be positive")
        
        retrieval_config = {
            "topk": topk,
            "score_threshold": score_threshold
        }
        
    except (ValueError, TypeError) as e:
        retrieval_config = None
        
    bot_response = await process_message(user_message, retrieval_config)
    bot_name = get_llm_name()
    return jsonify({'response': bot_response, 'name': bot_name})

    


UPLOAD_FOLDER = "/mnt/10TB/iordanissapidis/datasets/large"

@main.route('/SemanticRAG/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Ensure the file exists in the folder
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        # Return a 404 if the file does not exist
        abort(404)
        
        
@main.route('/SemanticRAG/pdf/<src>', methods=['GET'])
async def show_pdf(src):
    src_url = url_for('main.download_file', filename=src, _external=True)
    keywords = request.args.getlist('keyword')[:10]
    processed_keywords = [
        part for word in keywords for part in (word.split('\n') if '\n' in word else [word])
    ]

    keyword = ' '.join(processed_keywords)
    return render_template('components/pdf.html', src=src_url, keyword=keyword)
        
        
@main.route('/SemanticRAG/search', methods=['GET'])
async def search():
    return render_template('search.html')

@main.route('/SemanticRAG/search/<query>', methods=['GET'])
async def search_results(query):
    try:
        topk = int(request.args.get('topk'))
        score_threshold = float(request.args.get('score_threshold'))
        if topk <= 0 or score_threshold<= 0 : raise ValueError("topk value must be positive")
        documents = await search_query(query, topk, score_threshold)
        return render_template('components/search_results.html', documents=documents, keywords = query.split(' '))
    except (ValueError, TypeError) as e:
        documents = await search_query(query)
        return render_template('components/search_results.html', documents=documents, keywords = query.split(' '))
