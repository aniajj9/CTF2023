FROM alpine:3.9

# RUN apt-get update && apt-get install -y python3 python3-pip
RUN \
    apk update && \
    apk add python3 npm
COPY content/ /
WORKDIR /srv/app
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN \
    npm install && \
    npm run build

RUN apk del npm
WORKDIR /srv/app/build

EXPOSE 5000
CMD ["python3", "-m", "http.server", "5000"]
