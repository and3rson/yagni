PYTHON = python3

.PHONY: test
test:
	$(PYTHON) -m pytest yagni --verbose

.PHONY: build
build:
	rm -rf dist
	$(PYTHON) -m build

.PHONY: upload
upload: build
	twine upload dist/*
