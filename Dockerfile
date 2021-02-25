FROM python:3-slim

LABEL maintainer="cme@codeaffen.org"

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install -e .

EXPOSE 5876

ENTRYPOINT ["python", "-u", "/usr/local/bin/p3exporter"]
