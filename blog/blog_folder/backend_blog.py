from flask import Flask, request, jsonify
from generator import generate_blog
import os


app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def blog_endpoint():
    data = request.get_json()
    topic = data.get("topic", "")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    blog = generate_blog(topic)

    blog_folder = f"blogs/{topic.replace(" ", "_").lower()}.md"
    with open(blog_folder, "w") as f:
        f.write(blog)

    return jsonify({"message": "Blog generated successfully", "file": blog_folder, "blog": blog}), 200


    
if __name__ == "__main__":
    os.makedirs("blogs", exist_ok=True)
    app.run(host='0.0.0.0', port = 5000, debug=True)




    

