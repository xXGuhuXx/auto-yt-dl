# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL org.opencontainers.image.source="https://github.com/xXGuhuXx/yt-channel-dl"
WORKDIR /app
VOLUME /Downloads
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
RUN chmod a+x run.sh
CMD ["/app/run.sh"]
