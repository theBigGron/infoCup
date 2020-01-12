function distribute {
  scp slave.tar $1:/home/infocup/slave.tar
  ssh $1 '/usr/bin/docker load -i /home/infocup/slave.tar; \
    /usr/bin/docker stop $(docker ps -a -q);
    /usr/bin/docker run --restart=always -d slave:latest; \
    /usr/bin/docker run --restart=always -d slave:latest; \
    /usr/bin/docker run --restart=always -d slave:latest;'
}
docker save slave:latest > slave.tar
for server in "bagband"
do
 distribute $server
done