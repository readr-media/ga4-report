FROM gcr.io/google.com/cloudsdktool/cloud-sdk:slim

COPY .  /usr/src/app/ga4-report
WORKDIR  /usr/src/app/ga4-report

RUN addgroup user && adduser -h /home/user -D user -G user -s /bin/sh

RUN apt-get update \
    && apt-get install -y gcc libc-dev libxslt-dev libxml2 libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

ENV LC_ALL="en_US.utf8"

EXPOSE 8080
CMD ["env", "LC_ALL='en_US.utf-8'", "/usr/local/bin/uwsgi", "--ini", "server.ini"]
