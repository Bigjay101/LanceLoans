from getdata import get_data
from build_features import build_features
from test_df import test_feature_matrix
import pandas as pd
from sklearn.linear_model import LogisticRegression

df = get_data()
df = build_features(df)




def trainModel(df : pd.DataFrame):
    ''' Takes in cleaned and processed data, returns a trained model '''
    try:
        y = df['Default']
        df = df.drop(columns=['Default'])
        #training logic here

























        #evaluate model here

    except Exception as e:


        print(f"The following error has occured: {e}")






