## Feature Engineering & Feature Matrix Construction

This project places particular emphasis on robust feature engineering, with careful handling of missing data, categorical variables, and data leakage risks. The goal is to construct a final feature matrix that is fully numeric, model-ready, and explicitly encodes information about missingness where it is informative.

### 1. Design Principles

The feature-building process follows these guiding principles:

Models only consume numeric data: all string-based features are encoded before modeling.

Missingness can be informative: where appropriate, missing values are explicitly encoded rather than silently imputed.

Separation of concerns: exploratory analysis is kept separate from deterministic feature construction.

Reproducibility: feature transformations are implemented in a single function to ensure consistency across training and inference.

### 2. Handling Categorical Features

Categorical columns (e.g. Gender, Employment, Tier, res_type) are handled in two steps:

Missing value handling
Missing categorical values are replaced with an explicit "Missing" category. This prevents loss of rows and allows the model to learn whether missingness itself carries signal.

One-hot encoding
Categorical variables are converted to numerical form using one-hot encoding:

drop_first=True is used to avoid multicollinearity in linear models.

dummy_na=True ensures that missingness is still represented if any remains after preprocessing.

This results in binary indicator columns such as:

Gender_Male

Employment_Salaried

Tier_3

Gender_nan (if applicable)

The original string columns are removed after encoding.

### 3. Handling Numerical Features and Missing Data

Numerical features are processed using a missingness-aware strategy:

For each numerical column, a binary indicator column (<feature>_missing) is created to explicitly flag whether the value was originally missing.

Missing numerical values are imputed using a constant value (-1), chosen because it lies outside the valid domain of the original feature and is easily identifiable by the model.

This approach is particularly useful when:

Missing values are not missing at random (MNAR), or

The absence of data itself conveys information (e.g. no prior loan history).

Example transformation:

max_sanctioned_amount
→ max_sanctioned_amount
→ max_sanctioned_amount_missing

### 4. Dropped Columns

Certain columns are explicitly removed from the feature matrix:

Identifiers (e.g. ID, Dealer_code)
These carry no predictive signal and risk data leakage.

Non-feature metadata (e.g. DOB)
Either redundant or better handled via derived features (e.g. age).

Dropping these columns ensures the model does not learn spurious or non-generalizable patterns.

### 5. Final Feature Matrix Validation

Before modeling, the final feature matrix is validated to ensure:

No remaining object (string) columns

All features are numeric

Missingness is either encoded or explicitly imputed

The transformation is deterministic and reproducible

This guarantees compatibility with downstream machine learning models such as logistic regression or tree-based learners.

### 6. Rationale

This feature engineering strategy balances:

Interpretability (clear indicators for missing data),

Model performance (retaining informative missingness),

Practicality (simple, fast, and reproducible transformations).

It is particularly well-suited to structured, real-world datasets where missing values are common and often meaningful.