# Makefile for the Python Versioning project
# This has only been tested with GNU make from within the project root.

all: test coverage build doc

test:
	PYTHONPATH=src coverage run --module unittest discover

coverage:
	coverage report

build:
	./setup.py build

doc:
	$(MAKE) -C docs html

clean:
	$(MAKE) -C docs clean
	$(RM) -r build
	$(RM) -r htmlcov
	coverage erase
	git submodule update docs/_build/html
	git -C docs/_build/html checkout gh-pages

.PHONY: test coverage build doc clean
