# developer operations

help:
	$(info no default target)

env:
	pipenv --python 3.7
	pipenv install --dev

build:
	pipenv run python setup.py bdist_wheel sdist

install:
	pipenv install .

.PHONY: docs
docs:
	cd docs && make html
	cd docs && make man
	cp docs/build/man/* man/man1/

upload:
	pipenv run twine upload dist/*
