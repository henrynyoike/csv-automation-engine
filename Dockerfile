FROM python:3.12-slim

LABEL version=0.0.1
LABEL description="CSV Automation Engine"

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir pandas 
RUN pip install --no-cache-dir streamlit 
RUN pip install --no-cache-dir numpy 
RUN pip install --no-cache-dir scikit-learn

COPY . .

CMD ["streamlit" , "run" , "app.py"]

