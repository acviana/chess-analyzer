.PHONY: docs tests

check-updates:
	poetry update --dry-run | grep "Updating"

black:
	black chess_analyzer/
	black test/

black-diff:
	black chess_analyzer/ --diff
	black test/ --diff

docs:
	cd docs && make html

export:
	poetry export -f requirements.txt -o requirements.txt
	poetry export -f requirements.txt -o requirements_dev.txt --dev

pre-commit: black tests docs export

tests:
	pytest -vvs --cov-report term-missing --cov=chess_analyzer test/
