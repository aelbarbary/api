## Build the docker image

```
docker build -t ai-ticket .
```

## Run doker container

```
docker run -p 8000:8000 ai-ticket
```

## push docker image to docker hub

```
docker login -u aelbarba

docker build -t aelbarba/ai-chatbot:latest .

docker push aelbarba/ai-chatbot:latest

```
