# Solution

## PyTorch-Modell vom Master holen und solution bereistellen
```shell script
cd solution
rm -r pytorch_models
mkdir pytorch_models
curl localhost:8087/get-model > model.tar
tar -xf model.tar -C pytorch_models
cd ..
```

## Bauen und Starten des Docker-Containers
Mit 
```shell script
 docker build -t solution -f zSolution.Dockerfile .
```
kann das solutions-Projekt gebaut werden, dann
kann es mit

```shell script
 docker run -itd -p 50123:50123 --name sol1 solution:latest
```

gestartet werden.


## Starten der Visualisierung

Das solutions-Projekt kann mit dem Option `-vi`
mit aktivierter Visualisierung gestartet werden:
```shell script
 docker run -itd -p 50123:50123 --name sol1 solution:latest -vi
```

## Entfernen des Solution Docker Containers
Mit
```shell script
 docker stop sol1 && docker rm sol1
```
kann der gestartete solutions docker container gestoppt und entfernt werden. 

## Solution zu DockerHub pushen
Zunächst muss man sich bei dem DockerHub-Repository anmelden mit:
```shell script
docker login  --username=pgronau --password=5e3a7fe8-2d31-4a8e-ba1f-5782214a8556
```

Dann muss das `solution` image gebaut werden (siehe oben)
Um ein gebautes image mit obigem Befehl pushen zu können, muss es zunächst retagged werden mit:
```shell script
docker tag solution pgronau/infocup:solution
```

Gepushed werden kann es dann mit:
```shell script
docker push pgronau/infocup:solution
```

## Solution von DockerHub pullen
Zunächst muss man sich bei dem DockerHub-Repository anmelden mit:
```shell script
docker login  --username=pgronau --password=5e3a7fe8-2d31-4a8e-ba1f-5782214a8556
```

Pullt werden kann es dann mit:
```shell script
docker pull pgronau/infocup:solution
```

Nach dem pullen, kann es mit

```shell script
 docker run -itd -p 50123:50123 --name sol1 pgronau/infocup:solution
```
gestartet werden.