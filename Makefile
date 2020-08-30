.PHONY: docs test

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
	pytest --cov-report term-missing --cov=chess_analyzer test/
