from flask import Flask, request, jsonify
import openai
import base64
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return "Server is running."

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    image_data = base64.b64encode(file.read()).decode("utf-8")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "این تصویر را بررسی کن و گزارشی بده"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return jsonify({"response": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"error": str(e)})
