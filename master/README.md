# Master

## Bauen und Starten des Docker-Containers
Mit 
```shell script
 docker build -t master -f zMaster.Dockerfile .
```
kann das master-Projekt gebaut werden, dann
kann es mit

```shell script
 docker run -itd --restart=always -p 8087:8087 --name master master:latest
```
gestartet werden.

## Herunterladen der Modelle:
Nachdem die slaves 30 Spiele gespielt haben, wird das Modell trainiert und
dieses an den Master geschickt.
Der Master wiederum führt nach 2 Minuten, wenn noch kein Modell auf dem Master vorhanden ist
bzw. nach 20 Minuten, wenn schon 1 vorhanden ist die Modelle mit den,
letzen von den slaves geschickten, Modellen zusammen.
Das zusammengeführte Modell wird dann in der sqlite3 Datenbank gespeichert und kann mit
```shell script
curl localhost:8087/get-model > model.tar
```
ausgelesen werden.

## Hochladen von Modellen:
```bag1.tar``` ist eine Datei die folgende Dateien enthält:

1. ```actor.pth.tar```
2. ```actor_target.pth.tar```
3. ```critic.pth.tar```
4. ```critic_target.pth.tar```

```bash
curl  -F 'models=@/home/<USER>/Development/model_server/exampleModels/bag1.tar' localhost:8087/models --verbose -H "Authorization: Basic 11843e47-3e1b-45ba-9d09-2d154bb9a73l"
```

## Verändern der exploration rate:
Die Explorationsrate kann mit Werten
zwischen 0 und 1, wobei 0 Greedy ist, folgendermaßen verändert werden:

```bash
curl localhost:8087/set-exploration --verbose
```
