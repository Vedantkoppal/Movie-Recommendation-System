FROM python:3.11-slim

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=production 
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
