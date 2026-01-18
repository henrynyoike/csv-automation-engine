import streamlit as st

class Automator :
    def __init__(self):
        self.headers()
        
        self.left_sidebar()
    
    def headers(self):
        st.set_page_config(
            page_title='Excel & CSV Automation Engine',
        )
        
        st.markdown(
            f'''
            <h2 style = "margin-top : -8% ; margin-left:20% ; color:white ; opacity : 0.8">
            Excel & CSV Automation Engine
            </h2>
            ''' , 
        unsafe_allow_html=True)
        st.markdown(
            f'''
            <h6 style = "margin-top :-2% ; margin-left:22% ; color:grey">
            Automate cleaning , transformation and export of structured data
            </h6>
            ''' , 
        unsafe_allow_html=True)
    
    def left_sidebar(self):
        with st.sidebar as sides:
            st.header("📁 File Input")
            
            st.file_uploader('Upload Excel or CSV')
            
            st.header(' ⚙️ Automation Options')
        
            self.clean_data = st.checkbox('Clean data')
            self.rm_duplicates = st.checkbox('Remove Duplicates')
            self.normalize = st.checkbox('Normalize column names')

            st.header(' 📐 Transformations')
            
            self.encoder = st.checkbox('Encode Categorical columns')
            self.detect_dates = st.checkbox('Auto-detect dates')
            self.cast_nums = st.checkbox('Cast numeric columns')
            
            st.markdown('''
                <button style = "background-color:teal;
                opacity : 0.8 ;
                border-style:hidden;width:210px;border-radius:3px ; 
                ">Run Processing</button>
                ''' , unsafe_allow_html=True)
            
            file_name , duplicates , missing ='tests.xlsx' , 0 , 0
            
            if file_name :
                st.write(' Processing Logs')
                st.radio(' ' , options=f'Loaded {file_name}')
            
            st.markdown('''
            <button>Hi</button>''' , unsafe_allow_html=True)    
            
automator = Automator()       
        








