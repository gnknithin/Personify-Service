up-docker-dev:
	docker-compose -f ./docker-compose.dev.yml up -d --force-recreate --renew-anon-volumes
ps-docker-dev:
	docker-compose -f ./docker-compose.dev.yml ps
down-docker-dev:
	docker-compose -f ./docker-compose.dev.yml down --remove-orphans
up-docker-prod:
	docker-compose -f ./docker-compose.prod.yml up -d --force-recreate --renew-anon-volumes
ps-docker-prod:
	docker-compose -f ./docker-compose.prod.yml ps
down-docker-prod:
	docker-compose -f ./docker-compose.prod.yml down --remove-orphans
pytest-coverage:
	pytest -vv --cov --cov-report=term-missing
pytest-collect:
	pytest --collect-only
mypy:
	mypy .
ruff:
	ruff check .
ruff-fix:
	ruff check --fix .
pre-push: mypy ruff
install-testing-req:
	pip3 install pytest pytest-asyncio pytest-cov pytest-dotenv
install-linting-req:
	pip3 install autopep8 mypy ruff
install-req:
	pip3 install -r requirements.txt
upgrade-pip:
	pip3 install --upgrade pip
venv-remove:
	rm -rf .venv
venv-activate:
	source .venv/bin/activate
venv-setup:
	python3 -m venv .venv
clean-package:
	rm -Rf ./build; rm -Rf ./dist; rm -Rf ./.eggs; rm -Rf ./*.egg-info; rm -Rf ./**/*.egg-info; rm -Rf ./.coverage; 
clean-pycache:
	rm -Rf ./.pytest_cache; rm -Rf ./**/__pycache__; rm -Rf ./**/**/__pycache__; rm -Rf ./**/**/**/__pycache__; rm -Rf ./**/**/**/**/__pycache__;rm -Rf ./**/**/**/**/**/__pycache__;rm -Rf ./**/**/**/**/**/**/__pycache__;
clean: clean-package clean-pycache
install-dev-req: upgrade-pip install-linting-req install-testing-req install-req
install-prod-req: upgrade-pip install-req
run-dev-server:
	python3 src/server.py -p 8888 -c ./configs/development.yaml -d
run-unit-test:
	pytest -vv --cov --cov-report=term-missing ./tests/unit
run-integration-test:
	pytest -vv --cov --cov-report=term-missing ./tests/integration
run-e2e-test:
	pytest -vv --cov --cov-report=term-missing ./tests/e2e	