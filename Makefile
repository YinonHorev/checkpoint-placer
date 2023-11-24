lint:
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/
	mypy src/ tests/

test:
	pytest --cov=src --cov-report=term-missing --cov-fail-under=100 tests/
