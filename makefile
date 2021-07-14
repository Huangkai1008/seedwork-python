format:
	isort . && black . && flake8 .
test:
	pytest
coverage:
	coverage run -m pytest && coverage report -m
export-requirements:
	poetry export -f requirements.txt > requirements.txt --without-hashes
export-dev-requirements:
	poetry export -f requirements.txt > requirements-dev.txt --without-hashes --with dev
