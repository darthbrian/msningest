FROM python:3.7-alpine

RUN adduser -D msningest

WORKDIR /home/msningest

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN apk add --update --no-cache gcc libxslt-dev libc-dev
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn

COPY app app
COPY migrations migrations
COPY application.py config.py boot.sh ./
COPY .aws .aws
COPY key.pem key.pem
COPY cert.pem cert.pem
RUN chmod +x boot.sh

ENV FLASK_APP application.py

RUN chown -R msningest:msningest ./
USER msningest

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
