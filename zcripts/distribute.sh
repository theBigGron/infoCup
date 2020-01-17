#!/bin/bash
#for server in "bagband"
for server in "cleverns" "driefel" "etzel" "horsten" "ihlow" "jeringhave" "kranenkamp" "langendamm" "mariensiel" "neuenburg" # "funnix" "grabstede"

do
  echo $server
  scp ./docker_pw.txt $server:/home/infocup/docker_pw.txt
  ssh $server "
  /snap/bin/docker login --username pgronau -p \$(cat ~/docker_pw.txt) ;\
  /snap/bin/docker stop \$(/snap/bin/docker ps -a -q) ;\
  /snap/bin/docker rm \$(/snap/bin/docker ps -a -q) ;\
  echo 'y' | /snap/bin/docker image rm -a ;\
  /snap/bin/docker system prune -a ;\
  rm -r slave.tar ;\
  rm -r .cache/pip/;\
  /snap/bin/docker run --restart=always -d pgronau/infocup:slave; \
  /snap/bin/docker run --restart=always -d pgronau/infocup:slave; \
  /snap/bin/docker run --restart=always -d pgronau/infocup:slave; \
  /snap/bin/docker run --restart=always -d pgronau/infocup:slave; \
  "
done