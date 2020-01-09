# InformatikCup2020

## Repository Description
```
.
├── common
│   ├── d3t_agent
│   ├── data_processing
│   ├── __init__.py
│   ├── __pycache__
│   └── requirements.txt
├── master
│   ├── __init__.py
│   ├── MasterServer.py
│   ├── ModelMerger.py
│   ├── models.db
│   ├── __pycache__
│   ├── README.md
│   └── start.sh
├── slave
│   ├── ic20_linux
│   ├── __pycache__
│   ├── README.md
│   ├── src
│   └── start.sh
├── solution
│   ├── ic20_linux
│   ├── README.MD
│   ├── requirements.txt
│   └── TorchMain.py
├── venv
│   ├── bin
│   ├── include
│   └── lib
├── zcripts
│   ├── docker_scripts.MD
│   └── get_models.md
├── README.md
├── zMaster.Dockerfile
├── zSlave.Dockerfile
└── zSolution.Dockerfile

```  

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
