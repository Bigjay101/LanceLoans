from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, recall_score
from sklearn.impute import SimpleImputer
import numpy as np
import pandas as pd

# df = get_data()
# df = build_features(df)

def trainModel(df: pd.DataFrame):
    """
    Takes in cleaned & feature-engineered data
    Returns trained model and evaluation metrics
    """

    # 1. Split target and features
    y = df['default']
    X = df.drop(columns=['default'])

    # 2. Train-test split (STRATIFIED)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # 3. Impute numeric features (median)
    num_cols = X_train.columns

    imputer = SimpleImputer(strategy='median')
    X_train[num_cols] = imputer.fit_transform(X_train[num_cols])
    X_test[num_cols] = imputer.transform(X_test[num_cols])

    # 4. Train Logistic Regression with class weights
    model = LogisticRegression(
        class_weight='balanced',
        solver='liblinear',
        max_iter=1000
    )

    model.fit(X_train, y_train)

    # 5. Predict probabilities
    y_prob = model.predict_proba(X_test)[:, 1]

    # 6. Evaluate
    roc_auc = roc_auc_score(y_test, y_prob)

    # Temporary threshold (will tune later)
    y_pred = (y_prob >= 0.5).astype(int)
    recall = recall_score(y_test, y_pred)

    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"Recall (defaulters): {recall:.4f}")

    return model, roc_auc, recall
