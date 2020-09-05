FROM python:3.7-alpine

MAINTAINER Radhika Vyavahare "radhika.r.vyavahare@gmail.com"


WORKDIR /app

RUN pip3 install requests prometheus_client flask

COPY src/ /app

#ENTRYPOINT [ "python3" ]
EXPOSE 5000

CMD [ "python3","app.py" ]
