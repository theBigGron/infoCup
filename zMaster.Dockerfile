# zMaster.Dockerfile for Slave
# Base File
FROM debian:latest
RUN apt update
RUN apt install python3 python3-numpy python3-pip -y
RUN mkdir /home/app
RUN mkdir /home/app/src
##Copy requirements
WORKDIR /home/app/src
COPY common ./common/
RUN python3 -m pip install -r ./common/requirements.txt

# Master App
RUN apt install sqlite3 libsqlite3-dev -y
## Create empty sqlite hack
RUN /usr/bin/sqlite3 /home/app/models.db "create table et(f1 int); drop table et;"
RUN chmod 777 /home/app/models.db
## Copy src code
WORKDIR /home/app/
COPY master/README.md ./README.md
COPY master/start.sh ./start.sh
# move Merger to avoid module import conflicts
WORKDIR /home/app/src
COPY master/src/MasterServer.py ./MasterServer.py
RUN mkdir ./master
RUN mkdir ./master/src
COPY  master/src/ModelMerger.py ./master/src/ModelMerger.py
RUN touch ./master/__init__.py

WORKDIR /home/app

# Entrypoint
ENTRYPOINT ./start.sh