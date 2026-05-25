# train_model.py
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

def main():
    print("Loading Breast Cancer Wisconsin Dataset...")
    # Load dataset from scikit-learn
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target # 0 = malignant, 1 = benign

    print("Splitting data into training and testing sets...")
    # 80-20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Scaling features...")
    # SVM requires feature scaling for optimal performance
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Support Vector Machine (SVM) model...")
    # Initialize and train SVM classifier
    model = SVC(kernel='rbf', probability=True, random_state=42)
    model.fit(X_train_scaled, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    
    # Print metrics - focusing on Recall as false negatives are costly in medical contexts
    print("\n--- Model Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Malignant (0)', 'Benign (1)']))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nSaving model and scaler...")
    # Save the model and scaler using joblib
    joblib.dump(model, 'svm_cancer_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    print("Model saved successfully as 'svm_cancer_model.pkl'.")

if __name__ == "__main__":
    main()