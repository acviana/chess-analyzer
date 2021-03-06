.PHONY: build docs tests

build:
	poetry install

black:
	black chess_analyzer/
	black test/

black-diff:
	black chess_analyzer/ --diff
	black test/ --diff

docs:
	cd docs && make html

export-requirements:
	poetry export -f requirements.txt -o requirements.txt
	poetry export -f requirements.txt -o requirements_dev.txt --dev

flake8:
	flake8 chess_analyzer/ test/ --statistics

pre-commit: black flake8 tests docs export-requirements

tests:
	pytest -vvs --cov-report term-missing --cov=chess_analyzer test/

_update:
	poetry update

update: _update export-requirements

update-diff:
	poetry update --dry-run | grep "updat"
