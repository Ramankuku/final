import os
import argparse
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def model_fn(model_dir):
    """Load model for inference"""
    return joblib.load(os.path.join(model_dir, "model.joblib"))


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--random_state", type=int, default=42)

    # SageMaker specific arguments
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", "./output")
    )
    parser.add_argument(
        "--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "./model")
    )
    parser.add_argument(
        "--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "./train")
    )
    parser.add_argument(
        "--test", type=str, default=os.environ.get("SM_CHANNEL_TEST", "./test")
    )

    args, _ = parser.parse_known_args()

    # Ensure local folders exist for testing
    if not os.path.exists(args.train):
        raise ValueError(f"Training directory '{args.train}' does not exist.")
    if not os.path.exists(args.test):
        raise ValueError(f"Testing directory '{args.test}' does not exist.")

    # Load data
    train_df = pd.read_csv(os.path.join(args.train, "training_data.csv"))
    test_df = pd.read_csv(os.path.join(args.test, "testing_data.csv"))

    X_train = train_df.iloc[:, :-1]
    y_train = train_df.iloc[:, -1]
    X_test = test_df.iloc[:, :-1]
    y_test = test_df.iloc[:, -1]

    # Train model
    print("\nMODEL TRAINING STARTED...\n")
    model = RandomForestClassifier(
        n_estimators=args.n_estimators,
        random_state=args.random_state
    )
    model.fit(X_train, y_train)

    # Ensure model directory exists
    os.makedirs(args.model_dir, exist_ok=True)

    # Save model
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print("Model saved at:", model_path)

    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print("Test Accuracy **********:", test_acc)
