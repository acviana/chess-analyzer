black:
	black chess_analyzer/
	black test/

black-diff:
	black chess_analyzer/ --diff
	black test/ --diff

export:
	poetry export -f requirements.txt -o requirements.txt
	poetry export -f requirements.txt -o requirements_dev.txt --dev

pre-commit: black test export

.PHONY: test

test:
	pytest --cov-report term-missing --cov=chess_analyzer test/
