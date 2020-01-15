# Slave
## Bauen und Starten des Docker-Containers
Mit 
```shell script
 docker build -t slave -f zSlave.Dockerfile .
```
kann das slave-Projekt gebaut werden, dann
kann es mit

```shell script
 docker run -itd --name slave1 slave:latest
```
gestartet werden.

## Slaves zu DockerHub pushen
Zunächst muss man sich bei dem DockerHub-Repository anmelden mit:
```shell script
docker login  --username=pgronau --password=5e3a7fe8-2d31-4a8e-ba1f-5782214a8556
```

Dann muss das `slave` image gebaut werden (siehe oben)
Um ein gebautes image mit obigem Befehl pushen zu können, muss es zunächst retagged werden mit:
```shell script
docker tag slave pgronau/infocup:slave
```

Gepushed werden kann es dann mit:
```shell script
docker push pgronau/infocup:slave
```