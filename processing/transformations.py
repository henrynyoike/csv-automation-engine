import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import Normalizer , LabelEncoder

class Transformations :
    def __init__(self):
        self.df = DataFrame()

    def get_numerical_cols(self , data : DataFrame):
        cols = data.select_dtypes(include = [np.number]).columns
        return len(cols)

    def get_categorical_cols(self , data : DataFrame):
        cols = data.select_dtypes(include = ['object']).columns
        return len(cols)

    def normalize(self , data:DataFrame):
        # Get the Initial Arrangement of columns to retain it after normalization .
        col_arrangement = data.columns.to_list()

        numerical_cols = data.select_dtypes(include = ['int16' , 'int32',
                         'int64' ,'Int32' , 'float32' , 'float64' , 'float16'])
        # Get the names of the numerical columns
        numerical_names = numerical_cols.columns.to_list()

        categorical_cols = data.select_dtypes(include = ['object'])
        # Replace N/A rows with their mean for the Normalizer
        numerical_cols = numerical_cols.fillna(numerical_cols.mean())

        normalizer = Normalizer()

        # Normalize the numerical columns
        numerical_array = normalizer.fit_transform(numerical_cols)
        #Convert the array to a Dataframe
        numerical_cols = pd.DataFrame(numerical_array , columns = numerical_names)

        joined_df = pd.concat([categorical_cols , numerical_cols] , axis =1)
        joined_df = joined_df.reindex(columns =col_arrangement)

        return joined_df

    def encode_categorical(self , data : DataFrame):
        # Get the original column arrangement
        col_arrangement = data.columns.to_list()

        # Get the categorical and numerical columns
        num_cols = data.select_dtypes(include = ['int64' , 'int32' , 'float32' , 'float64'])
        categorical_cols = data.select_dtypes(include = ['object'])

        # Create the encoder
        encoder = LabelEncoder()

        # Encode the categorical columns
        for col in categorical_cols.columns :
            categorical_cols[col] = encoder.fit_transform(categorical_cols[col])

        # Combine the two dataframes
        joined_df = pd.concat([num_cols , categorical_cols] , axis = 1)

        # Get the original arrangement of columns in the dataframe
        df = joined_df.reindex(columns = col_arrangement)

        return df

    def replace_na_mean(self , data :DataFrame):
        # Get the original arrangement
        col_arrange = data.columns.to_list()

        #Get the numerical and categorical_columns
        num_cols , cat_cols = data.select_dtypes(['int64' , 'int32' , 'float32' , 'float64']) , data.select_dtypes(["object"])
        #Fill numerical N/A with mean
        num_filled = num_cols.fillna(num_cols.mean())

        # Combine the dataframes
        df_comb = pd.concat([num_filled , cat_cols] , axis=1)

        #Rearrange the columns with the original arrangement
        df = df_comb.reindex(columns = col_arrange)

        return df


