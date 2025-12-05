from flask import Flask, request, jsonify, render_template
import random
import os
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

backup_fortunes = ["The universe said 'maybe', which is honestly better than 'no'."]

#routes

@app.route("/")
def home():
    return render_template('fortune.html')
@app.route("/fortune", methods =["POST"])
def fortune():
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    if data is None:
        return jsonify({"error": "You must send JSON"}), 400
    
    name = data.get("name", "").strip()
    question = data.get ("question","").strip()

    #data validation

    if not name and not question :
        return jsonify({"error ":"The astros can't tell your fortune without your name also make sure to ask a question!"}), 400
    
    #fortune cookie
    try:
        prompt = f"""
        You are a mystical, sarcastic, funny, fortune teller.
        Always respond with a humorous prophecy.
        Keep it to 1-3 sentences maximum
        
        Name :{name}
        Question :{question}
        """

        response = client.chat.completions.create(
          model ="llama-3.3-70b-versatile",
          messages =[{"role":"user", "content": prompt}]
         )

        fortune_cookie = response.choices[0].message.content

    except Exception as e:
         print("Groq API failed:", e)  
         fortune_cookie = random.choice(backup_fortunes)

     
    return jsonify({"fortune": fortune_cookie})

if __name__ == "__main__":
    app.run(debug=True)