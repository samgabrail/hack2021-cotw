# docker build -t samgabrail/cotw:latest .
# docker push samgabrail/cotw:latest
FROM python:3.8.12-slim-bullseye
LABEL maintainer="Sam Gabrail"
WORKDIR /app
COPY . /app
RUN apt-get update && pip install -r requirements.txt && groupadd -g 1000 appuser && useradd -m -r -u 1000 -g appuser appuser 
USER appuser
CMD [ "python", "-u", "main.py" ]