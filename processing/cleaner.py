import pandas as pd
import numpy as np
import os
from pandas import DataFrame

'''
Clean Data
'''
class Cleaner :
    def __init__(self , data : DataFrame):
        self.data : DataFrame = data
    
    def remove_na(self , data : DataFrame) -> DataFrame:
        data = data.dropna()
        return data
    
    def get_na_rows(self) -> int :
        #Get the initial len and the final length and subtract
        initial_len = len(self.data)
        cleaned = self.data.dropna()
        na_rows = initial_len - len(cleaned)
        
        return na_rows
    
    def get_percentage_missing(self):
        na_rows = self.get_na_rows()
        all_rows = len(self.data)
        
        #Get the percentage of missing valiues in rows to the whole data
        missing_percentage = (na_rows / all_rows) * 100 
        
        return missing_percentage 

    def remove_duplicates(self , data : DataFrame) -> DataFrame:
        data = data.drop_duplicates()
        return data
    
    def get_duplicate_rows(self) -> int:
        initial_len = len(self.data)
        cleaned = self.data.drop_duplicates()
        duplicates_len = initial_len - len(cleaned)
        
        return duplicates_len

    def get_negative_rows(self , data : DataFrame) -> int:
        data = data.select_dtypes(include = [np.number])

        negatives = 0
        for index , row in data.iterrows():
            for num in list(row):
                if num != np.abs(num):
                    negatives += 1

        return negatives

    def get_absolutes(self , data : DataFrame):
        '''Get the absolute values of negative numbers'''
        numerical_cols = data.select_dtypes(include = [np.number]).columns

        data[numerical_cols] = data[numerical_cols].abs()

        return data
