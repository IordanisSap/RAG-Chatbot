from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort, redirect, url_for, flash
from .chatbot.chat import process_message, get_llm_name, search_query, get_vectorstores, index_documents
from .utils import validate_path

import os
import tempfile
import shutil

main = Blueprint('main', __name__, url_prefix='/SemanticRAG')

DOWNLOAD_FOLDER = "/mnt/10TB/iordanissapidis/SemanticRAG"


@main.route('/')
def menu():
    return render_template('menu.html')

@main.route('/conversation', methods=['POST'])
def conversation():
    messages = request.json.get('messages')
    print(messages)
    return render_template('components/conversation.html', messages=messages)

@main.route('/passages', methods=['POST'])
def relevant_studies():
    relevant = request.json.get('passages')
    query = request.json.get('query')
    return render_template('components/search_results.html', documents=relevant, keywords=query.split(' '))

    
@main.route('/chat', methods=['GET'])
def chatUI():
    print(get_vectorstores())
    return render_template('chat.html')

@main.route('/chat', methods=['POST'])
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


@main.route('/pdf/<collection>/<src>', methods=['GET'])
async def show_pdf(collection, src):
    src_url = url_for('main.download_file', collection=collection, filename=src, _external=True)
    # src_url = url_for('main.download_file', filename=src, _external=True, _scheme='https')
    keywords = request.args.getlist('keyword')[:10]
    processed_keywords = [
        part for word in keywords for part in (word.split('\n') if '\n' in word else [word])
    ]

    keyword = ' '.join(processed_keywords)
    return render_template('components/pdf.html', src=src_url, keyword=keyword)
       
 
@main.route('/search', methods=['GET'])
async def search():
    vectorstores = get_vectorstores()
    return render_template('search.html', collections=vectorstores)

@main.route('/search/<query>', methods=['GET'])
async def search_results(query):
    collection = request.args.get('collection')
    try:
        topk = int(request.args.get('topk'))
        score_threshold = float(request.args.get('score_threshold'))
        if topk <= 0 or score_threshold<= 0 : raise ValueError("topk value must be positive")
        documents = await search_query(query, collection, topk, score_threshold)
        return render_template('components/search_results.html', collection=collection, documents=documents, keywords = query.split(' '))
    except (ValueError, TypeError) as e:
        documents = await search_query(query, collection)
        return render_template('components/search_results.html', collection=collection, documents=documents, keywords = query.split(' '))



@main.route('/download/<collection>/<filename>', methods=['GET'])
def download_file(collection, filename):
    print(DOWNLOAD_FOLDER, validate_path(collection, filename))
    try:
        return send_from_directory(DOWNLOAD_FOLDER, validate_path(collection, filename), as_attachment=False)
    except (FileNotFoundError, ValueError):
        abort(404)
        
@main.route('/collection/<name>', methods=['GET'])
async def get_documents(name):
    try:
        path = validate_path(DOWNLOAD_FOLDER, name)
        docs = os.listdir(path)
        return render_template("components/documents.html", collection=name, documents=docs)
    except ValueError:
        return []
    
@main.route('/collection', methods=['GET'])
async def get_collections():
    try:
        return os.listdir(DOWNLOAD_FOLDER)
    except ValueError:
        return []
        
UPLOAD_FOLDER = "/mnt/10TB/iordanissapidis/SemanticRAG/tmp"
ALLOWED_EXTENSIONS = {'pdf'}


@main.route('/upload', methods=['POST'])
async def upload_files():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    temp_dir = tempfile.mkdtemp(dir=UPLOAD_FOLDER)
    print(f"Temporary directory created: {temp_dir}")

    if 'files[]' not in request.files:
        flash('No files part')
        return redirect(request.url)

    files = request.files.getlist('files[]')
    saved_files = []
    
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(temp_dir, filename)
            file.save(filepath)
            saved_files.append(filepath)
        else:
            flash(f"Invalid file type: {file.filename}")


    await index_documents(temp_dir, "test")
    shutil.rmtree(temp_dir)
    return {"uploaded_files": saved_files}, 200