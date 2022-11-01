LINE_LENGTH=120

# Install

install-run:
	pip install --upgrade pip
	pip install -r requirements.txt

install-test:
	pip install -r requirements-test.txt
	@make install-run --no-print-directory

install-dev:
	pip install -r requirements-dev.txt
	pip install -r requirements-lint.txt
	@make install-test --no-print-directory
	#sudo apt-get install gettext
	pre-commit install

install: install-dev
	@make test --no-print-directory
	@make lint --no-print-directory

# Test
test:
	echo "TODO"

# Lint

format:
	black .
	isort .

check-black:
	black --check .

check-isort:
	isort --check .

check-flake8:
	flake8 .

check-pylint:
	pylint git_syncer/ --fail-under=9

check-mypy:
	mypy git_syncer/

lint: format
	pre-commit run --all-files

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
