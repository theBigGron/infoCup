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