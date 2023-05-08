FROM python:3.9.16-slim-buster
COPY . /home
RUN pip install Flask requests
WORKDIR ./home
ENV FLASK_APP=app.py
EXPOSE 9003
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9003"]