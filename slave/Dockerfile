FROM debian:latest
RUN apt update
RUN apt install python3 python3-numpy python3-pip -y
RUN mkdir /home/app
#Copy requirements
WORKDIR /home/app/pyton
ADD ./python/requirements.txt ./requirements.txt
RUN python3 -m pip install -r requirements.txt
# Copy App
WORKDIR /home/app/
COPY . .
ENTRYPOINT ./start.sh