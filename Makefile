# Makefile for the Python verschemes project
# This has only been tested with GNU make from within the project root.

SHELL := /bin/bash

all: coverage build doc

test:
	PYTHONPATH=src coverage run --branch --module unittest discover
	# doctest does not work on docs/examples.rst in Python 2.
	if [[ `python -c 'import sys; print(sys.version_info[0])'` = 3 ]]; then PYTHONPATH=src python -m doctest docs/examples.rst; fi

coverage: test
	coverage report

coverage_html: test
	coverage html

build:
	./setup.py build

readme:
	cat README_editable.rst | ( while read; do if [[ $${REPLY#.. include:: } != $${REPLY} ]]; then cat $${REPLY#.. include:: }; else echo $${REPLY}; fi; done ) > README.rst

doc: readme
	$(MAKE) -C docs html

clean:
	./setup.py clean -a
	$(MAKE) -C docs clean
	$(RM) MANIFEST
	$(RM) -r dist
	$(RM) -r htmlcov
	coverage erase
	find . -type d -name '__pycache__' | xargs $(RM) -r
	find . -type f -name '*.py[co]' | xargs $(RM)
	git submodule update docs/_build/html
	git -C docs/_build/html checkout gh-pages

.PHONY: test coverage coverage_html build readme doc clean
