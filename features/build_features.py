import pandas as pd

def changeTypes(df):
    float_cols = [ 'max_mob',
       'num_bounced_repaying', 'EMI', 'Loan_Amount', 'Tenure', 'Dealer_code',
        'no_advanceEmi_paid', 'interest',
       'age', 'max_sanctioned_live',
       'sanctioned_amt_sercured', 'sanctioned_amt_uunsecured',
       'max_sanctioned_twoWheeler', 'last_loan', 'first_loan']
    df[float_cols] = df[float_cols].astype('float64')
    int_cols = ['ID', 'bounce_first_EMI', 'num_bounce_12m', 'num_loans', 'num_secured',
       'num_unsecured','num_newLoans_3m','num_30d_pastDue_6m', 'num_60d_pastDue_6m', 'num_90d_pastDue_3m','default']
    df[int_cols] = df[int_cols].astype('Int64')

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    changeTypes(df)
    


    # 1. Fill categorical strings with 'Missing'
    str_cols = ['Gender','res_type','Employment','Product_code_two_wheeler','Tier']
    for col in str_cols:
        df[col] = df[col].fillna('Missing')

    # 2. Drop irrelevant columns
    df = df.drop(columns=['ID', 'DOB', 'Dealer_code'], errors='ignore')

    # 3. One-hot encode categorical columns (missing captured via dummy_na=True)
    encoded_cols_categorical = ['Product_code_two_wheeler','Gender','Employment','res_type','Tier']
    df = pd.get_dummies(
        df,
        columns=encoded_cols_categorical,
        drop_first=True,
        dummy_na=True
    )

    # 4. Handle numeric columns (original numeric columns only)
    categorical_cols = df.select_dtypes(include=['str']).columns
    df = df.drop(columns=categorical_cols)

    numeric_cols = df.select_dtypes(include=['int64', 'float64','Int64']).columns
    for col in numeric_cols:
        if col != 'default':
            df[f'{col}_missing'] = df[col].isna().astype(int)
            df[col] = df[col].fillna(-1)
        
    
    
    return df



