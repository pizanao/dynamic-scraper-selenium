.PHONY: install test compile demo scrape
install:
	python -m pip install -r requirements.txt
test:
	pytest
compile:
	python -m compileall app tests
demo:
	python -m app.cli serve-demo --host 127.0.0.1 --port 5000
scrape:
	python -m app.cli scrape --base-url http://127.0.0.1:5000 --output-dir output
