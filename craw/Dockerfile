FROM python:3.9.16-slim-buster
COPY . /craw
RUN pip install fastapi uvicorn pandas beautifulsoup4 schedule requests
WORKDIR ./craw
CMD ["uvicorn", "crawData:app", "--host", "0.0.0.0", "--port", "9001"]
