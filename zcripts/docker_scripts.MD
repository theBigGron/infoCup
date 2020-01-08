
Start master, open port
```bash
docker run --restart=always -p 8087:8087 master:latest
```
start slave, force restart on termination
``` bash
docker run -d --restart=always slave:latest
```
copy models db from master to host
``` bash
docker cp 9c73f3c19580:/home/app/models.db .
```
show events, like restarts of containers
``` bash
docker events
```
stop restarting of container
``` bash
docker update --restart=no my-container
```
