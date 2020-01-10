#!/bin/bash
for server in "bagband" "cleverns" "driefel" "etzel" "horsten" "ihlow" "jeringhave" "kranenkamp" "langendamm" "mariensiel" "neuenburg" # "funnix" "grabstede"

do
  echo $server
  scp ./docker_pw.txt $server:/home/infocup/docker_pw.txt
  ssh 'docker cat ~/docker_pw.txt | docker login --username pgronau --password-stdin; \
  docker run -d pgronau/infocup:slave; \
  docker run -d pgronau/infocup:slave; \
  docker run -d pgronau/infocup:slave; \
  docker run -d pgronau/infocup:slave; \'
done