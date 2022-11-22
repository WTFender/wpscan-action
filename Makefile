IMAGE_NAME=fiixwpscan

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME) .

.PHONY: run
run-docker:
	@docker run \
		-e SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL} \
		-e WP_SCAN_API_TOKEN=${WP_SCAN_API_TOKEN} \
		$(IMAGE_NAME) entrypoint.sh "https://www.fiixsoftware.com/"

.PHONY: install
install:
	@echo "Installing locally";
	@python3 -m virtualenv -p python3 env && . env/bin/activate && pip install -r src/requirements.txt

.PHONY: test
test:
	@. env/bin/activate && PYTHONPATH=$(shell pwd )/src/ pytest -s tests/
