FROM python:3.11-slim

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_ENV=production 
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w","4","-b","0.0.0.0:8000", "main:app"]
