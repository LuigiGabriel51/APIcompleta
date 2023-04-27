FROM python:3.10

EXPOSE 5000

WORKDIR /D:\vscode\python\projeto\projeto_PIBIT\APIcompleta
COPY . .

RUN pip install jwt && pip install Flask-Login &&  pip install twilio && pip install mysql-connector

CMD ["python3", "main.py"]

