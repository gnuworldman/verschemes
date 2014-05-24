# Makefile for the Python Versioning project
# This has only been tested with GNU make from within the project root.

all: test build doc

test:
	PYTHONPATH=src coverage run --source=src --module unittest discover && coverage report

build:
	./setup.py build

doc:
	$(MAKE) -C docs html

clean:
	$(MAKE) -C docs clean
	$(RM) -r build
	$(RM) -r htmlcov
	coverage erase

.PHONY: build
