LINE_LENGTH=120

# Setup

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt -r requirements-dev.txt

# Linting

lint:
	black . -l $(LINE_LENGTH)
	@make check-lint --no-print-directory

check-lint:
	black . -l $(LINE_LENGTH) --check
	flake8 . --max-line-length=$(LINE_LENGTH) --exclude __init__.py
	mypy . --ignore-missing-imports

# Test

test:
	echo "TODO"

# Pypi

build:
	gio trash -f dist/
	python -m build

upload:
	twine upload dist/*

upload-test:
	twine upload --repository testpypi dist/*

# Quick and dirty

amend:
	make lint
	git add .
	git commit --amend --no-edit
	git push -f
