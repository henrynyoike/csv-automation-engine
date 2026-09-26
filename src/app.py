import streamlit as st
import pandas as pd
from pandas import DataFrame
import os , sys
import numpy as np
import matplotlib.pyplot as plt

# Append the system to the outer base directory
current_dir = os.getcwd()
outer_dir = os.path.dirname(current_dir)

sys.path.append(outer_dir)

from processing.cleaner import Cleaner
from processing.loader import Logs
from processing.transformations import Transformations

# Append back to the current directory
sys.path.append(current_dir)

# The Automator class
class Automator :
    def __init__(self):
        self.df = DataFrame()
        self.transformer = Transformations()
        self.headers()
        self.left_sidebar()

        if self.uploaded_file:
            self.top_summary()
            self.data_preview()
            self.processes_tabs()

    def headers(self):
        st.set_page_config(
                page_title='CSV Automation Engine',
        )

        st.markdown(
            f'''
            <h2 style = "margin-top : -8% ; margin-left:30% ; color:white ; opacity : 0.8">
            CSV Automation Engine
            </h2>
            ''' ,
        unsafe_allow_html=True)
        st.markdown(
            f'''
            <h6 style = "margin-top :-2% ; margin-left:25% ; color:grey">
            Automate cleaning , transformation and export of structured data
            </h6>
            ''' ,
        unsafe_allow_html=True)

    def left_sidebar(self):
        cols = st.columns(2)

        with st.sidebar:
            st.header("📁 File Input")

            self.uploaded_file = st.file_uploader('Upload CSV' , type = ['csv'])

            if self.uploaded_file:
                self.processing_logs()

    def processing_logs(self):
        st.divider()

        st.header(' ⚙️ Automation Options')

        self.clean_missing = st.checkbox('Remove missing values')
        self.rm_duplicates = st.checkbox('Remove Duplicates')
        self.remove_neg_nums = st.checkbox('Absolute negative numbers')

        st.header(' 📐 Transformations')

        self.normalize = st.checkbox('Normalize column names')
        self.encoder = st.checkbox('Encode Categorical columns')
        self.mean_missing = st.checkbox('Replace missing values with Mean')

    def data_preview(self):
        #Get the uploads directory or create if does not exist
        UPLOADS = 'Uploads'

        os.makedirs(UPLOADS , exist_ok=True)

        file_name = self.uploaded_file.name

        file_save_path = os.path.join(UPLOADS , file_name)

        with open(file_save_path , 'wb')as f:
            f.write(self.uploaded_file.getbuffer())

        if file_name.endswith('csv'):
            self.df : DataFrame= pd.read_csv(file_save_path)

        else :
            self.df : DataFrame = pd.read_excel(file_save_path)

        return self.df

    def top_summary(self):
        df = self.data_preview()

        col1 , col2 , col3 , col4 = st.columns([10,10,10,10])

        self.cleaner = Cleaner(self.df)
        logs = Logs(self.df)

        self.total_rows , self.total_cols = logs.total_rows_cols()
        self.missing_rows = self.cleaner.get_na_rows()
        self.duplicates = self.cleaner.get_duplicate_rows()

        with col1:
            st.markdown('''
                        <p style = "font-size:270%;color:red">📄</p>
                                ''' , unsafe_allow_html=True)

            st.markdown(f'''
                <h6 style = "text-indent:40%;margin-top:-50%;margin-left:-10% ;
                font-size:110%">{self.total_rows:,}</h3>
                    ''' , unsafe_allow_html=True)

            st.markdown('''
                <h6 style = "font-size:90%;margin-left:35%;margin-top:-40%;
                color:grey">Total Rows<h6/>

                    ''' , unsafe_allow_html=True)

        with col2 :
            st.markdown('''
                        <p style = "font-size:55px;margin-top:-6%;color:white;opacity:0.7">🗄</p>
                                ''' , unsafe_allow_html=True)

            st.markdown(f'''
                <h6 style = "text-indent:40%;margin-top:-57%;margin-left:-10% ;
                font-size:110%">{self.total_cols:,}</h3>
                    ''' , unsafe_allow_html=True)

            st.markdown('''
                <h6 style = "font-size:90%;margin-left:35%;margin-top:-50%;
                color:grey">Columns<h6/>

                    ''' , unsafe_allow_html=True)

        with col3:
            st.markdown('''
                        <p style = "font-size:300% ; color: orange;opacity:0.9">⚠</p>
                                ''' , unsafe_allow_html=True)

            st.markdown(f'''
                <h6 style = "text-indent:40%;margin-top:-58%;margin-left:-10% ;
                font-size:110%">{self.missing_rows}</h3>
                    ''' , unsafe_allow_html=True)

            st.markdown('''
                <h6 style = "font-size:90%;margin-left:35%;margin-top:-45%;
                color:grey">Missing Rows<h6/>

                    ''' , unsafe_allow_html=True)
        with col4 :
            st.markdown('''
                        <p style = "font-size:300%;color:yellow;opacity:0.9">🛢</p>
                                ''' , unsafe_allow_html=True)

            st.markdown(f'''
                <h6 style = "text-indent:40%;margin-top:-58%;margin-left:-10% ;
                font-size:110%">{self.duplicates:,}</h3>
                    ''' , unsafe_allow_html=True)

            st.markdown('''
                <h6 style = "font-size:90%;margin-left:35%;margin-top:-50%;
                color:grey">Duplicates<h6/>

                    ''' , unsafe_allow_html=True)

        st.dataframe(self.df)

    def cleaner_tab(self , df):
        cleaner = Cleaner(self.df)

        st.write(f'✅ Loaded file : {self.file_name}')
        if self.rm_duplicates :
            df = cleaner.remove_duplicates(df)
            st.write(f' ✅ Removed {self.duplicates} duplicate rows' if self.duplicates > 0 else '❌ No duplicates found')

        if self.clean_missing :
            if not self.mean_missing:
                df = cleaner.remove_na(df)
                st.write(f'✅ Handled {self.missing_values} missing values' if self.missing_values > 0 else '❌ No missing values')

        if self.remove_neg_nums :
            df = cleaner.get_absolutes(df)
            st.write(f'✅ Replaced {self.negative_nums} Negative numbers with their absolutes' if self.negative_nums > 0 else '❌ No negative values')

        return df

    def transform_tab(self , df):
        transformer = Transformations()

        if self.mean_missing :
            num_cols = transformer.get_numerical_cols(df)
            self.df = transformer.replace_na_mean(df)
            st.write(f'✅ Replaced the N/A values of {num_cols} columns with mean' if num_cols > 0 else '❌ No Numerical Columns to Convert N/A to Mean')

        if self.normalize :
            df = transformer.normalize(df)
            st.write(f'✅ Normalised {self.normalised_cols} columns ' if self.normalised_cols > 0 else '❌ No Columns to normalize')

        if self.encoder :
            df = transformer.encode_categorical(df)
            st.write(f'✅ Encoded {self.encoded} columns with categorical numbers' if self.encoded > 0 else '❌ No Columns to Encode')

        return df

    def visuals(self , data : DataFrame):
        cols = data.columns
        chart_types = ['Line','Bar' , 'Area' , 'Scatter' , 'Map']
        x_col = st.selectbox('X-Axis' , cols)
        y_col = st.selectbox('Y-Axis' , cols)
        chart = st.selectbox('Chart Type' , chart_types)

        x = data[x_col].to_list()
        y = data[y_col].to_list()

        df = pd.DataFrame({'X':x , 'y':y})
        if chart == "Line":
             st.line_chart(df.set_index('X'))
        if chart == "Bar":
             st.bar_chart(df.set_index('X'))
        if chart == "Area":
             st.area_chart(df.set_index('X'))
        if chart == "Scatter":
             st.scatter_chart(df.set_index('X'))
        if chart == "Map":
            try:
                st.map(df.set_index('X'))
            except:
                st.write("Error : Cannot find Latitude and Longitudes ")

    def final_data(self , df):
        df = self.cleaner_tab(df)
        df = self.transform_tab(df)

        st.dataframe(df)

        if self.uploaded_file.name.endswith('csv'):
                st.download_button(label = 'Download as CSV' ,
                                data = df.to_csv() ,
                                file_name = f'processed_{self.uploaded_file.name}')

    def processes_tabs(self):
        self.file_name , self.missing_values = self.uploaded_file.name , self.cleaner.get_na_rows()
        self.negative_nums , self.normalised_cols = self.cleaner.get_negative_rows(self.df) , self.transformer.get_numerical_cols(self.df)
        self.encoded = self.transformer.get_categorical_cols(self.df)

        tab1 , tab2 , tab3  , tab4  = st.tabs(['Data Cleaning' , 'Transformations' , 'Visualisation' , 'Final Data'] )

        with tab1:
            self.cleaner_tab(self.df)

        with tab2 :
            self.transform_tab(self.df)

        with tab3 :
            self.visuals(self.df)

        with tab4 :
            self.final_data(self.df)

if __name__ == "__main__":
    automator = Automator()

