from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort, redirect, url_for, flash
from .chatbot.chat import process_message, search_query, get_vectorstores, index_documents, get_tmp_dir, get_doc_dir
from .utils import validate_path

import os
import tempfile
import shutil

main = Blueprint('main', __name__, url_prefix='/SemanticRAG')

DOWNLOAD_FOLDER = get_doc_dir()


@main.route('/')
def menu():
    vectorstores = get_vectorstores()
    return render_template('default.html', collections=vectorstores)


# ------------------- Templates -------------------

@main.route('/conversation', methods=['POST'])
def conversation():
    messages = request.json.get('messages')
    print(messages)
    return render_template('components/conversation.html', messages=messages)

@main.route('/passages', methods=['POST'])
def relevant_studies():
    relevant = request.json.get('passages')
    query = request.json.get('query')
    collection = request.json.get('collection')

    return render_template('components/search_results.html', collection=collection, documents=relevant, keywords=query.split(' '))


@main.route('/pdf/<collection>/<src>', methods=['GET'])
async def show_pdf(collection, src):
    # src_url = url_for('main.download_file', collection=collection, filename=src, _external=True)
    src_url = url_for('main.download_file', collection=collection, filename=src, _external=True, _scheme='https')
    keywords = request.args.getlist('keyword')[:10]
    processed_keywords = [
        part for word in keywords for part in (word.split('\n') if '\n' in word else [word])
    ]

    keyword = ' '.join(processed_keywords)
    return render_template('components/pdf.html', src=src_url, keyword=keyword)
       

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


# ------------------- API -------------------


@main.route('/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    collection = request.json.get('collection')

    try: 
        topk = int(request.args.get('topk'))
        score_threshold = float(request.args.get('score_threshold'))
        if topk <= 0 or score_threshold <= 0 : raise ValueError("topk value must be positive")
        
        retrieval_config = {
            "topk": topk,
            "score_threshold": score_threshold,
        }
        
    except (ValueError, TypeError) as e:
        retrieval_config = None
        
    bot_response = await process_message(user_message, collection, retrieval_config)
    return jsonify(bot_response)


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
        

@main.route('/collection', methods=['POST'])
async def upload_collection():
    
    UPLOAD_FOLDER = get_tmp_dir()
    ALLOWED_EXTENSIONS = {'pdf'}
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    temp_dir = tempfile.mkdtemp(dir=UPLOAD_FOLDER)
    print(f"Temporary directory created: {temp_dir}")
    
    new_name = request.form.get("name")

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


    await index_documents(temp_dir, new_name)
    shutil.copytree(temp_dir, os.path.join(DOWNLOAD_FOLDER,new_name), dirs_exist_ok=True)
    shutil.rmtree(temp_dir)
    return redirect(url_for('main.menu'))