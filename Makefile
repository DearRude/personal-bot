.EXPORT_ALL_VARIABLES:

SHELL=/bin/bash
pyver = "3.8.0"

include .env
export $(grep -v '^#' .env | xargs)


installpoet:
	@echo --- INSTALLING ---
	@python -V
	@printf "${pyver}\n`python -V | cut -d" " -f2`" | sort -V | head -n1 | grep -q ${pyver} || echo "You need Python ${pyver} or newer"
	@poetry --version || pip install poetry --user
	@poetry install

install:
	pip install -r requirements.txt

run:
	@echo --- RUNNING BOT ---
	@poetry run python src/main.py

req:
	@pip freeze > requirements.txt

reqpoet:
	@poetry export -f requirements.txt > requirements.txt

