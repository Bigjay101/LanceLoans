# LanceLoans – Loan Default Prediction Model


## Modeling Approach

### Why Logistic Regression?
- Interpretable and regulator-friendly
- Strong baseline for credit risk modeling
- Produces probability scores for flexible decision thresholds
- Performs well with imbalanced data when combined with class weighting

---

## Training Pipeline

The model training is implemented in the `trainModel` function and follows these steps:

### 1. Feature and Target Split
- `X`: all engineered features
- `y`: default indicator

---

### 2. Stratified Train-Test Split
- 80% training / 20% testing
- Stratification preserves the original default rate in both datasets

This prevents biased evaluation caused by class imbalance.

---

### 3. Missing Value Imputation
- Median imputation applied to numeric features
- Imputer is fit on training data only
- Prevents data leakage

---

### 4. Model Training
A Logistic Regression model is trained with:
- `class_weight = 'balanced'` to handle class imbalance
- `solver = 'liblinear'`
- `max_iter = 1000` to ensure convergence

This setup emphasizes correct identification of defaulters.

---

### 5. Probability Prediction
The model outputs predicted probabilities:
- `P(default = 1)`

This allows threshold tuning instead of relying on a fixed cutoff.

---

### 6. Model Evaluation

#### ROC-AUC
- Measures ranking ability across all thresholds
- Appropriate for imbalanced datasets
- Indicates how well the model separates defaulters from non-defaulters

#### Recall (Defaulters)
- Measures the proportion of actual defaulters correctly identified
- Calculated using a temporary probability threshold of 0.5
- Threshold will be tuned based on business objectives

---

## Current Model Performance

- **ROC-AUC:** ~0.81  
- **Recall (Defaulters):** ~0.68  

These results indicate strong predictive power for a baseline credit risk model.

---

## Key Design Decisions
- No synthetic oversampling (e.g. SMOTE) to avoid data leakage
- Class weighting used to handle imbalance
- Focus on ROC-AUC and Recall instead of accuracy
- Probability-based outputs to support risk policy decisions

---

## How to Run

```python
model, roc_auc, recall = trainModel(df)
