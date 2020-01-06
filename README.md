docker run --restart=always -p 8087:8087 master:latest

docker run -d --restart=always slave:latest

docker cp 9c73f3c19580:/home/app/models.db .

docker events

docker update --restart=no my-container
