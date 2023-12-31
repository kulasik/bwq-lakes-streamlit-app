FROM python:3.10-slim

WORKDIR usr/src/app

COPY requirements.txt ./

RUN apt-get update \
    && apt-get install -y openjdk-17-jre \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

ENV KAGGLE_USERNAME=''
ENV KAGGLE_KEY=''
ENV STREAMLIT_SERVER_PORT=80

EXPOSE 80

COPY . .

CMD ["streamlit", "run", "Hello.py"]