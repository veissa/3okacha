FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY start.sh .
RUN chmod +x start.sh

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["./start.sh"]

