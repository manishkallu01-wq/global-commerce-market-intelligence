.PHONY: test validate scale sample all

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_project.py

scale:
	python3 scripts/estimate_scale.py --profile production

sample:
	PYTHONPATH=. python3 scripts/run_sample_pipeline.py

all: test validate scale sample
