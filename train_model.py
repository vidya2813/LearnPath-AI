
import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Find dataset.csv in the same folder as this Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "learnpath_model.joblib")

# Load dataset
data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")
print("\nFirst five rows:")
print(data.head())

# Features used to make predictions
features = [
    "python_level",
    "quiz_score",
    "study_minutes",
    "goal"
]

target = "recommended_category"

# Check required columns
required_columns = features + [target]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns in dataset: {missing_columns}"
    )

# Prepare input and output
X = data[features]
y = data[target]

# Check the dataset
if len(data) < 5:
    raise ValueError("Please provide more training examples.")

if X.isnull().any().any() or y.isnull().any():
    raise ValueError(
        "The dataset contains empty values. Please clean it first."
    )

# Split data to evaluate the model
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create and train the model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate on data not used for training
predictions = model.predict(X_test)

print("\nModel evaluation")
print("----------------")
print("Test accuracy:", round(accuracy_score(y_test, predictions), 2))

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

# Train the final model using all available examples
model.fit(X, y)

# Save model and required feature order
joblib.dump(
    {
        "model": model,
        "features": features,
        "categories": sorted(y.unique().tolist())
    },
    MODEL_PATH
)

print("\nModel trained using all dataset rows.")
print("Saved model to:", MODEL_PATH)

# Test a sample prediction
sample = pd.DataFrame(
    [[1, 70, 45, 1]],
    columns=features
)

result = model.predict(sample)[0]

print("\nSample input:", sample.iloc[0].to_dict())
print("Sample recommendation:", result)
