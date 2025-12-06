from flask import Flask, request, render_template, jsonify
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import re

app = Flask(__name__)

MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
FAISS_INDEX = faiss.read_index("faiss_qna.index")
QNA_DF = pd.read_csv('Cleaned_QnA.csv')

def clean_text(text):
  text = str(text).lower()
  text = re.sub(r'[^a-zA-Z0-9\s]','',text)
  text = re.sub(r'\s+'," ",text)
  return text

def get_similar_answer(query, k=1):
    cleaned_query = clean_text(query)
    query_embedding = MODEL.encode([cleaned_query]).astype('float32')
    distances, indices = FAISS_INDEX.search(query_embedding, k)
    
    results = []
    for i in range(k):
        distance_score = float(distances[0][i])
        
        if distance_score > 1.2:
            results.append({
                'question': 'No Good Match Found',
                'answer': "I'm sorry, I don't have information on that specific topic in my database. I can only answer questions related to the mental health data I was trained on.",
                'distance': distance_score
            })
        else:
            df_index = indices[0][i]
            row = QNA_DF.iloc[df_index]
            results.append({
                'question': row['Question'],
                'answer': row['Answer'],
                'distance': distance_score
            })
            
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    query = ""
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            crisis_keywords = ['suicide', 'self-harm', 'kill myself', 'die']
            if any(word in query.lower() for word in crisis_keywords):
                 crisis_answer = {
                    'question': 'CRISIS ALERT',
                    'answer': 'If you are in immediate danger or distress, please contact a professional immediately. This bot is for educational purposes only. Call the National Suicide Prevention Lifeline at 988 (in the US) or emergency services in your country.',
                    'distance': 0.0
                 }
                 results = [crisis_answer]
            else:
                results = get_similar_answer(query)

    return render_template('index.html', results=results, query=query)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query')
    if query:
        crisis_keywords = ['suicide', 'self-harm', 'kill myself', 'die']
        if any(word in query.lower() for word in crisis_keywords):
             return jsonify([{
                'question': 'CRISIS ALERT',
                'answer': 'If you are in immediate danger, please contact emergency services. Call 988 or your local emergency number immediately.',
                'distance': 0.0
             }])
        
        results = get_similar_answer(query)
        return jsonify(results)
    
    return jsonify({'error': 'No query provided'})

app.run(debug=True)