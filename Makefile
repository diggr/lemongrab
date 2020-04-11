.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Run software tests
	python -m pytest $(PYTEST_ARGS)

.PHONY: black
black: ## Format the code
	python -m black lemongrab

.PHONY: flake
flake: ## Flake8 the code
	flake8 --max-line-length=99 lemongrab

.PHONY: check
check: flake ## Perform black and flake checks (Should be done pre-commit)
	python -m black --check lemongrab
