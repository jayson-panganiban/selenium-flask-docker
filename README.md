# CAR API
-----------------------

### Usage

1. Reopen project in docker container
2. In bash terminal, run python main.py


### Endpoints

**/car/query**

*make only*
```
curl -iX GET "http://127.0.0.1:5001/car/query?make=ALFA+ROMEO"
```

*model only*
```
curl -iX GET "http://127.0.0.1:5001/car/query?model=CR-V+LX"
```

*make and model*
```
curl -iX GET "http://127.0.0.1:5001/car/query?make=MITSUBISHI&model=LANCER+EVO"
```

*year/s*
```
curl -iX GET "http://127.0.0.1:5001/car/query?year=1965"
curl -iX GET "http://127.0.0.1:5001/car/query?year=2020&year=2019&year=2018"
```

*make, model, year/s*
```
curl -iX GET "http://127.0.0.1:5001/car/query?make=AUDI&model=A3+PREMIUM&year=2020&year=2019"
```

**/car/lot/{lot_id}**
*returns car information via lot id*
```
curl -iX GET "http://127.0.0.1:5001/car/lot/40234580"
```

**/car/member/lot/{lot_id}**
*returns complete car information via lot id*
```
curl -iX GET "http://127.0.0.1:5001/car/member/lot/40234580"
```