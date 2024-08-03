.PHONY: build
build:
	rm -rf dist
	python3 -m build

.PHONY: upload
upload: build
	twine upload dist/*
