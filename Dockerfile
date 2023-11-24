FROM python:3.12-slim

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY ./src .

CMD ["python3", "app.py"]
