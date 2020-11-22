
[![tests](https://github.com/angru/abilling/workflows/tests/badge.svg)](https://github.com/angru/abilling/actions?query=workflow%3Atests+branch%3Amaster++)
[![codecov](https://codecov.io/gh/angru/abilling/branch/master/graph/badge.svg)](https://codecov.io/gh/angru/abilling)

## Run tests
```shell script
make test
```

## Run service
```shell script
make run
```

documentation available on [local machine](http://localhost:5000/docs)


## ToDo

* Add `IdempotencyKey` if necessary. Like [tome](https://docs.tome.ru/idempotency), [Яндекс.Касса](https://yookassa.ru/developers/using-api/basics#idempotence) did
* Full body responses rather then 204 status codes
* More detailed data about client
* Operation type in separate table not enum
