from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open("D:\\FinalProjects\\Loan_Prediction\\src\\Notebook\\tree_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Extract features safely
        income = data.get("Income", 0)
        cc_avg = data.get("CCAvg", 0)
        education = data.get("Education", 0)
        mortgage = data.get("Mortgage", 0)
        cd_account = data.get("CD_Account", 0)

        features = np.array([[income, cc_avg, education, mortgage, cd_account]])
        prediction = model.predict(features)

        result = "Approved" if prediction[0] == 1 else "Denied"
        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    # Run on port 8000 since your client is calling that
    app.run(host="0.0.0.0", port=8000, debug=True)
