FROM alpine:3

LABEL maintainer="cme@codeaffen.org"

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN apk update && \
    apk add python3 py3-pip build-base python3-dev linux-headers && \
    pip3 install -e . && \
    apk del py3-pip build-base python3-dev linux-headers

EXPOSE 5876

ENTRYPOINT ["python3", "-u", "/usr/bin/p3exporter"]
