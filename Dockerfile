FROM ubuntu:20.04

WORKDIR /workspace
COPY . .

RUN chmod +x scripts/*
RUN sh scripts/install.sh
RUN sh scripts/test.sh

EXPOSE 80 443 3306 5000 8080 33060

ENV FLASK_ENV development
CMD /workspace/scripts/start.sh