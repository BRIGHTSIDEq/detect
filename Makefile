.PHONY: test prepare benchmark train evaluate export validate
prepare:
	python scripts/prepare_dataset.py
test:
	pytest
benchmark:
	python scripts/benchmark.py
train:
	python scripts/train.py
evaluate:
	python scripts/evaluate.py
export:
	python scripts/export_coreml.py
validate:
	python scripts/validate_coreml.py
