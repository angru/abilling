PYTHON = 3.9.0
ENV_NAME = abilling

env:  # is not working right now
	pyenv virtualenv ${PYTHON} ${ENV_NAME} && \
	pyenv activate ${ENV_NAME} && \
	pyenv local ${ENV_NAME} && \
	poetry install && \
	pre-commit install

test:
	docker-compose run --entrypoint "python -m pytest -vvs" abilling-test

run:
	docker-compose up abilling
