# Master

Hochladen von Modellen:
```bag1.tar``` ist eine Datei die folgende Dateien enthält:

1. city_actor.pth.tar
2. city_actor_target.pth.tar
3. city_critic.pth.tar
4. city_critic_target.pth.tar
5. disease_actor.pth.tar
6. disease_actor_target.pth.tar
7. disease_critic.pth.tar
8. disease_critic_target.pth.tar

Diese Dateien werden von der Abgabe inkludiert und enthalten die Daten um das Neuronale Netz mit gelernten Werten zu initialisieren.

```bash
curl  -F 'models=@/home/pag/Development/model_server/exampleModels/bag1.tar' localhost:8087/models --verbose -H "Authorization: Basic 11843e47-3e1b-45ba-9d09-2d154bb9a73l"
```

Download der Modelle:
```bash
curl localhost:8087/get-model --verbose
```

Verändern der exploration rate (Werte zwischen 0 und 1, wobei 0 Greedy ist):
```bash
curl localhost:8087/set-exploration --verbose
```
