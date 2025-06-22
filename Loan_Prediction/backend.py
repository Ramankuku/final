from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

model_path = os.path.join(os.path.dirname(__file__), "src", "Notebook", "tree_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        income = data['Income']
        cc_avg = data['CCAvg']
        education = data['Education']
        mortgage = data['Mortgage']
        cd_account = data['CD Account']

        features = np.array([[income, cc_avg, education, mortgage, cd_account]])
        prediction = model.predict(features)

        result = "Approved" if prediction[0] == 1 else "Denied"
        return jsonify({"prediction": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
