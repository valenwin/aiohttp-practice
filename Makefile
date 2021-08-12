.PHONY: all \
		setup \
		run \

venv/bin/activate: ## alias for virtual environment
	python -m venv venv

setup: venv/bin/activate ## project setup
	. venv/bin/activate; pip install pip==21.0.1 wheel setuptools
	. venv/bin/activate; pip install --exists-action w -Ur requirements.txt

run: venv/bin/activate ## run project
	. venv/bin/activate; python entry.py -c ./local.yaml --reload --port 8000

# Migration commands
revision: venv/bin/activate ## Create new db revision
	. venv/bin/activate; python entry.py --revision --config=local.yaml
db: venv/bin/activate ## Apply migrations
	. venv/bin/activate; python entry.py --migrate --config=local.yaml
show: venv/bin/activate ## Show migrations
	. venv/bin/activate; python entry.py --show --config=local.yaml
downgrade: venv/bin/activate ## Downgrade db migration
	. venv/bin/activate; python entry.py --downgrade --config=local.yaml

flake:
	flake8 api --max-line-length 100

black:
	black api

mypy:
	mypy api
