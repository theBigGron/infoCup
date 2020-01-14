# Solution

## PyTorch-Modell vom Master holen und solution bereistellen
```shell script
cd solution
rm -r pytorch_models
mkdir pytorch_models
curl localhost:8087 > model.tar
tar -xf model.tar -C pytorch_models
```

## Bauen und Starten des Docker-Containers
Mit 
```shell script
 docker build -t solution -f zSolution.Dockerfile .
```
kann das solutions-Projekt gebaut werden, dann
kann es mit

```shell script
 docker run -itd --restart=always --name sol1 solution:latest
```

gestartet werden.

Mit der Option `-it` des obigen `docker run`-Befehls, veranlasst den Docker Container
im Interaktiven Modus zu sein, sodass mit

```shell script
 docker attach sol1
```

zu dem Docker Container verbunden werden kann.
Mit `STRG-P STRG-Q` kann dann der Container wieder detached werden
und das verbundene Terminal verlassen werden.


## Starten der Visualisierung
