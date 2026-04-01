.PHONY: run validate-run show-agenda

run:
	ralph run --config ralph.yml

validate-run:
	@if [ -z "$(RUN)" ]; then echo "Usage: make validate-run RUN=runs/<run_id>"; exit 1; fi
	python3 scripts/validate_run.py $(RUN)

show-agenda:
	@sed -n '1,240p' state/agenda.md

