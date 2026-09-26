import pandas as pd
from pandas import DataFrame

class Logs :
    def __init__(self , data : DataFrame):
        self.data = data
    
    def total_rows_cols(self):
        total_rows = len(self.data)
        total_cols = len(self.data.columns)
        
        return int(total_rows) , int(total_cols)
    
    
        

















