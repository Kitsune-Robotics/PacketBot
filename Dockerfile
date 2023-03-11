FROM python:3.10

LABEL maintainer="kenwood364@gmail.com"

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY packetbot.py /app
COPY entrypoint.sh /app

ENTRYPOINT ["./entrypoint.sh"]