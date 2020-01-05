FROM debian:latest
RUN apt update
RUN apt install python3 python3-numpy python3-pip -y
RUN mkdir /home/app
WORKDIR /home/app
COPY . .
RUN python3 -m pip install -r ./python/requirements.txt
ENTRYPOINT ./start.sh