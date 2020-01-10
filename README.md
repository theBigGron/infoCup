# InformatikCup2020

## Overview
Wir sind eine Gruppe aus vier Studenten der Universität Oldenburg, die am InformatiCup 2020 der Gesellschaft
für Informatik (GI) teilnehmen. Die diesjährige Aufgabe bestand daraus die Menscheit vor dem Aussterben durch
tödliche Krankheiten in einer Simulationsumgebung zu bewahren (Pandemie). Wir haben uns dazu entschieden
unser Lösung auf Künstlicher Intelligenz aufzubauen.

Die GI hat die Simulation als einen Webclient (ic20) zur Verfügung gestellt, der HTTP-GET Anfragen an einen zu
implementierenden Webserver schickt. Wir haben den Webserver mit Flask in Python3 gebaut.

Der slave-Webserver nimmt Anfragen des ic20 Webclients an und Trainiert das in commons spezifierte Modell.
Nach einer gewissen Zeit werden die Modell an den master-Webserver geschickt, der diese annimmt
(dafür muss commons Dateien auch im master zur Verfügung stehen) und in eine sqlite3 Datenbank schreibt.
Nachdem das Modell traniert wurde, wird es durch das solution Package gesichert im Nicht-Trainingsmodus
bereitgestellt.

Die Anwendungen selber laufen mit den jeweilig richtigen Source Dateien in Docker Containern, dafür
ist für jede Anwendung ein eigenes Dockerfile spezifiert. Nachfolgend ist beschrieben wie sie
fürs Debugging auch lokal (ohne docker) ausgeführt werden können.

## Anleitungen
[Anleitungen für Master](master/README.md)<br/>
[Anleitungen für Slave](slave/README.md)<br/>
[Anleitungen für Solution](solutions/README.md)

## Build Project
### Manually
0. Install python3 and python3-dev on Ubuntu with
```sh
sudo apt-get install python3 python3-dev
```
1. Install virtualenv globally with
```sh
sudo -H pip3 install virtualenv
```
2. Create an virtual environment and source it with:
```sh
virtualenv venv -p python3.6
source venv/bin/activate
```
3. Install requirements with:
```sh
python3 -m pip install -r requirements.txt
```

### Freeze pip requirements
In order to be able to install all required dependencies, freeze
the pip3-dependencies to requirements.txt with
```sh
python3 -m pip freeze > requirements.txt
```
### With Docker [Deprecated]
Run
```sh
docker image build -t informaticup:1.0 .
```
inside `informatiCup2020`-dir.

## Deployment

Es gibt zwei Applikationen um die Modelle zu trainieren. Es gibt dabei unterschiedliche Docker Container die gestartet werden müssen. Es gibt einen Master, welcher zuerst gestartet werden muss. Der Master verwaltet die Modelle der Slave Modelle. Dann können die Slave Modelle gestartet werden.

Im Ordner common findet sich der Code welcher von sowohl von dem Server,
als auch von den Client-Applikationen verwendet wird.

### Docker commands
Starten des Master Containers.
```
docker run --restart=always -p 8087:8087 master:latest
```
Starten des slave Containers.
```
docker run -d --restart=always slave:latest
```
```
docker cp 9c73f3c19580:/home/app/models.db .
```
```
docker events
```
```
docker update --restart=no my-container
```

## Create/Run Tests

All tests has to remain in `tests/`-dir and has to follow
the pattern `test_*.py`.
Then you can run the tests with
```sh
python3 -m unittest discover -s tests
```
within project root dir `informaticup2020`.

Alternatively you can add a PyCharm `Unittests`-configuration:
1. choose `Unittests > Custom`
2. Add `discover -s tests` to `Additional Arguments`
3. Choose your project root dir as `Working directory`
