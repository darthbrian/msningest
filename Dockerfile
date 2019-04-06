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
COPY msningest.py config.py boot.sh ./
COPY .aws .aws
RUN chmod +x boot.sh

ENV FLASK_APP msningest.py

RUN chown -R msningest:msningest ./
USER msningest

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
