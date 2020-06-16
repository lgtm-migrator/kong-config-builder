.PHONY: install setup lint test kong integration all-tests check-sec

install:
	@pip install -e .

setup: install
	@pip install -r requirements_test.txt

lint:
	@flake8 kong_config_builder tests_unit tests_integration

test:
	@pytest --ignore="tests_integration"

kong:
	@python create_test_config.py
	@docker build -t kong_config_builder:test .
	@docker run -d -p 8080:80 -p 8081:8001 kong_config_builder:test

integration:
	@pytest --ignore="tests_unit"

coverage:	
	@pytest --cov=kong_config_builder --cov-report=term-missing

all-tests: | coverage lint check-sec

check-sec:
	@echo "Running Bandit..."
	@bandit -r .
