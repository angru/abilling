
[![tests](https://github.com/angru/abilling/workflows/tests/badge.svg)](https://github.com/angru/abilling/actions?query=workflow%3Atests+branch%3Amaster++)
[![codecov](https://codecov.io/gh/angru/abilling/branch/master/graph/badge.svg)](https://codecov.io/gh/angru/abilling)

## Run tests
```shell script
make test
```

## Run service
```shell script
# will serve on http://localhost:5000
make run
```

## Documentation

documentation available on [local machine](http://localhost:5000/docs)


## ToDo

* Add `IdempotencyKey` if necessary. Like [tome](https://docs.tome.ru/idempotency), [Яндекс.Касса](https://yookassa.ru/developers/using-api/basics#idempotence) did
* Full body responses rather than 204 status codes
* More detailed data about client
* Operation type in separate table not enum
* Add description to validators fields
* More tests. Coverage means nothing


## Rationale

* PostgreSQL - because I think C and A more important than P in that case
* FastAPI - because IO bound task

## Cons

* Without `IdempotencyKey` transactions can duplicate because of network issues
* Data model is over-simplified
* Operation type implemented as enum in table transaction. Better solution is separate table


## Pros

* Scalability(horizontal) - mean application, database it's different story
* Asynchronous - pretty fast for that type of task


## API

Create client
```shell script
curl --location --request POST 'localhost:5000/clients' \
--header 'Content-Type: application/json' \
--data-raw '{"name": "Oleg"}'
```

Get client info
```shell script
curl --location --request GET 'localhost:5000/clients/1'
```

Add funds to wallet
```shell script
curl --location --request POST 'localhost:5000/charges' \
--header 'Content-Type: application/json' \
--data-raw '{"wallet_id": 1, "amount": "10.5"}'
```

Transfer funds

```shell script
curl --location --request POST 'localhost:5000/transfers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "wallet_from": 1,
    "wallet_to": 2,
    "amount": "10.01"
}'
```
