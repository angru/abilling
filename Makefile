PYTHON = 3.9.0
ENV_NAME = abilling

env:
	pyenv virtualenv ${PYTHON} ${ENV_NAME}
	pyenv local ${ENV_NAME}
	poetry install

test:
	docker-compose run --entrypoint "python -m pytest -vvs" abilling-test

run:
	docker-compose up abilling