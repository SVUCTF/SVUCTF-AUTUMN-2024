FROM python:3.12-alpine

WORKDIR /app

COPY app/ .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. *.proto

CMD ["python", "server.py"]
