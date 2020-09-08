# CAR API

### Usage

1. Reopen project in docker container or build and run
```
docker build -t selenium-flask -f Dockerfile
docker run -d -p 5001:5001 selenium-flask
```

### Endpoints

**/car/query**

*make only*
```
curl -iX GET "http://127.0.0.1:5001/car/query?make=ALFA+ROMEO"
```
