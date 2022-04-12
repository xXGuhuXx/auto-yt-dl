# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
LABEL org.opencontainers.image.source="https://github.com/xXGuhuXx/auto-yt-dl"
ENV UMASK=000
ENV UID=99
ENV GID=100
ENV DATA_PERM=770
WORKDIR /app
VOLUME /app/Downloads
VOLUME /app/data
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
RUN chmod a+x run.sh
CMD ["/app/run.sh"]
