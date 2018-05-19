FROM python:3.6

ENV PYTHONIOENCODING UTF-8

EXPOSE 8000

ADD requirements.txt /app/
ADD requirements /app/requirements

WORKDIR /app/
RUN pip install -r /app/requirements.txt

ADD . /app/

RUN chmod +x /app/compose/start.sh
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]