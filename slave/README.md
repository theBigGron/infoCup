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
