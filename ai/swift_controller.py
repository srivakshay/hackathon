from flask import Flask, request, jsonify
import os

from ai import bedrockprompt, bedrock_claude_langchain
from utils import extract_table_names, prompts

app = Flask(__name__)

# Configurations (e.g., for upload folder)
UPLOAD_FOLDER = '../data_dir'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'store_proc.txt' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['store_proc.txt']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"message": "File successfully uploaded", "filename": file.filename}), 200


@app.route("/generate", methods=["GET"])
def generate():
    return jsonify({"message": bedrockprompt.covert_to_spring_boot("../data_dir/upload")}), 200


@app.route('/getdomaintables', methods=['GET'])
def get_domain_tables():
    return jsonify({"message": prompts.get_domain_ui_prompt_from_file("../data_dir/upload")}), 200


@app.route("/generate_tech_doc", methods=["GET"])
def generate_tech_doc():
    return jsonify(
        {"message": bedrock_claude_langchain.query_code("Generate technical documentation", "../data_dir/upload")}), 200


@app.route("/generate_business_doc", methods=["GET"])
def generate_business_doc():
    return jsonify(
        {"message": bedrock_claude_langchain.query_code("Generate business documentation without any technical details",
                                                        "../data_dir/upload")}), 200


@app.route("/ask", methods=["GET"])
def ask_any_thing():
    return jsonify(
        {"message": bedrock_claude_langchain.query_code(request.args.get("query"),
                                                        "../data_dir/upload")}), 200


if __name__ == '__main__':
    app.run(debug=True)
