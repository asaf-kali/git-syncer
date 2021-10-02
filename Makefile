amend:
	make lint
	git add .
	git commit --amend --no-edit
	git push -f

lint:
	black . -l 120

build:
	gio trash -f dist/
	python -m build

upload:
	twine upload dist/*

upload-test:
	twine upload --repository testpypi dist/*
