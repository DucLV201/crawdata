FROM python:3.9.16-slim-buster
COPY . /mysql_api
RUN pip install fastapi uvicorn mysql-connector-python requests
WORKDIR ./mysql_api
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9002"]