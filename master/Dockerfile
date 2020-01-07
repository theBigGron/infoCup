FROM debian:latest
RUN apt update
RUN apt install python3 python3-numpy python3-pip sqlite3 libsqlite3-dev -y
# Install Python Requirements
RUN mkdir /home/app/
WORKDIR /home/app/
ADD ./python/requirements.txt /home/app/python/requirements.txt
WORKDIR /home/app/python
RUN python3 -m pip install -r requirements.txt
# Create empty sqlite hack
RUN /usr/bin/sqlite3 /home/app/models.db "create table et(f1 int); drop table et;"
RUN ls -la /home/app/models.db
RUN chmod 777 /home/app/models.db
RUN ls -la /home/app/models.db
# Copy src code
WORKDIR /home/app/
COPY ./README.md ./README.md
COPY ./start.sh ./start.sh
COPY ./python/*.py ./python/
ENTRYPOINT ./start.sh