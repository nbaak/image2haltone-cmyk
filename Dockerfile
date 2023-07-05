FROM python:3.10.2

RUN apt-get update && apt-get upgrade -y
 
RUN python -m pip install --upgrade pip
RUN python -m pip install Flask Pillow

RUN mkdir /application && cd /application

COPY ./src /application

RUN groupadd -r app -g 1000 && \
    useradd -u 1000 -r -g app -s /sbin/nologin -c "Docker image user" app && \
    chown -R 1000:1000 /application

USER app

EXPOSE 5000
WORKDIR /application
ENTRYPOINT ["./start.sh"]
