FROM python:3.6-alpine

LABEL maintainer="Janusz Kawczynski <jk70250@gmail.com>"

RUN apk add --no-cache \
        nginx \
        supervisor \
        gcc \
        linux-headers \
	musl-dev

RUN pip install uwsgi
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN mkdir -p /run/nginx
COPY nginx-app.conf /etc/nginx/conf.d/default.conf
COPY supervisor-app.ini /etc/supervisor.d/

COPY requirements.txt /srv/app/
RUN pip install -r /srv/app/requirements.txt

COPY . /srv/app/

EXPOSE 80
CMD ["supervisord", "-n"]
