import pandas as pd
from .build_features import build_features
import unittest as ut
from ..data.getdata import get_data

def test_df(df: pd.DataFrame, original_df: pd.DataFrame = None):
    """
    Tests a feature matrix for ML readiness.

    Parameters
    ----------
    df : pd.DataFrame
        The processed feature matrix to test.
    original_df : pd.DataFrame, optional
        Original dataframe, used to verify missing indicators.
    target_col : str, optional
        Name of target column, if present.
    """
    print("============================================================================================================================================ FINAL DF TEST REPORT ============================================================================================================================================\n")

    # 1. Shape
    print(f"Shape of feature matrix: {df.shape}\n")

    # 2. Remaining missing values
    total_missing = df.isnull().sum().sum()
    print(f"Total missing values in matrix: {total_missing}")
    if total_missing > 0:
        print(df.isnull().sum()[df.isnull().sum() > 0])
    print()

    # 3. Column types
    print("Column types:")
    print(df.dtypes.value_counts())
    print()

    # 4. Missingness indicators (if original_df provided)
    if original_df is not None:
        missing_cols = [c for c in df.columns if c.endswith('_missing')]
        for col in missing_cols:
            orig_col = col.replace('_missing', '')
            if orig_col in original_df.columns:
                correct = (df[col] == original_df[orig_col].isna().astype(int)).all()
                print(f"Missing indicator check for {col}: {correct}")
        print()

    # 5. Inspect dummy variables
    dummy_cols = [c for c in df.columns if '_' in c and df[c].nunique() <= 2]
    if dummy_cols:
        print(f"Dummy variables detected ({len(dummy_cols)} columns). Sample values:")
        print(df[dummy_cols].head())
    print()

    print(df.info())

    print("============================================================================================================================================ END OF REPORT ============================================================================================================================================")


# df = your processed feature matrix
# original_df = the raw DataFrame before preprocessing
# target_col = 'target' if you have one

df_raw = get_data()
df = build_features(df_raw)
test_df(df, original_df=df_raw)
