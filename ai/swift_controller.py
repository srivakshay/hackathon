import io
import zipfile

from flask import Flask, request, jsonify, safe_join, send_file, abort
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


@app.route('/download', methods=['GET'])
def download_file():
    try:
        # Directory containing files to be zipped
        directory = os.path.join(app.root_path, '../download')

        # Check if the directory exists
        if not os.path.exists(directory):
            abort(404)  # Return a 404 error if the directory is not found

        # Create a zip file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory)
                    zf.write(file_path, arcname)

        memory_file.seek(0)

        return send_file(memory_file, attachment_filename='files.zip', as_attachment=True)
    except Exception as e:
        print(f"Error: {e}")
        abort(500)  # Return a 500 error if something goes wrong


if __name__ == '__main__':
    app.run(debug=True)
