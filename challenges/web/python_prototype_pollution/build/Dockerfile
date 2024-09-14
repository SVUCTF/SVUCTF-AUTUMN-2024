FROM python:3.12-alpine

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py /app/main.py
COPY app/static/index.html /app/static/index.html
COPY app/static/index-compiled.js /app/static/index-compiled.js

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
