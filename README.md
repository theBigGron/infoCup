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
ist für jede Anwendung ein eigenes Dockerfile spezifiert. Nachfolgend ist beschrieben, wie Sie
fürs Debugging auch lokal (ohne docker) ausgeführt werden können.

## Bauen des Projektes
### Manuell
0. Installieren von python3 und python3-dev unter Ubuntu mit
```sh
sudo apt-get install python3 python3-dev
```
1. Virtualenv global installieren mit
```sh
sudo -H pip3 install virtualenv
```
2. Eine virtuelle Umgebung erstellen und source mit:
```sh
virtualenv venv -p python3.6
source venv/bin/activate
```
3. Projektabhängigkeiten installieren mit:
```sh
python3 -m pip install -r requirements.txt
```

## Deployment
Zuerst muss der Master gestartet werden, dann können
beliebig viele Slaves gestartet werden, die das Spiel
mit der ic20 spielt. Das so gewonnene Modell im Master,
kann dann für das Solutions-Projekt bereitgestellt werden.
Dieses trainiert dann nicht mehr mit der ic20 Simulation
und hat die Visualisierung, hat aber weiter sonst durch
das commons-Projekt den gleichen Code.

## Anleitungen
[Anleitungen für Master](master/README.md)<br/>
[Anleitungen für Slave](slave/README.md)<br/>
[Anleitungen für Solution](solution/README.md)

### Docker commands
**Hinweis:**
Mit der Option `-it` eines `docker run`-Befehls, veranlasst den Docker Container
im Interaktiven Modus zu starten, sodass mit

```shell script
 docker attach <name>
```

zu dem Docker Container verbunden werden kann.
Mit `STRG-P STRG-Q` kann dann der Container wieder detached werden
und das verbundene Terminal verlassen werden.

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

## Über uns
* Markus Gersdorf <Markus.Gersdorf@uni-oldenburg.de>
* Paul Gronau <Paul.Gronau@uni-oldenburg.de>
* Torben Logemann <Torben.Logemann@uni-oldenburg.de>
* Marcel Peplies <Marcel.Peplies@uni-oldenburg.de>

# Dokumentation
Für weitere Informationen siehe [Dokumentation](https://cloudstorage.uni-oldenburg.de/s/gHKaaBdBWogWLF7)
