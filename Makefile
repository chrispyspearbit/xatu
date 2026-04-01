.PHONY: run validate-run promote-backlog show-agenda show-discovered

run:
	ralph run --config ralph.yml

validate-run:
	@if [ -z "$(RUN)" ]; then echo "Usage: make validate-run RUN=runs/<run_id>"; exit 1; fi
	python3 scripts/validate_run.py $(RUN)

promote-backlog:
	@if [ -z "$(CANDIDATES)" ]; then echo "Usage: make promote-backlog CANDIDATES=runs/<run_id>/follow_on_candidates.json"; exit 1; fi
	python3 scripts/promote_backlog.py $(CANDIDATES)

show-agenda:
	@sed -n '1,240p' state/agenda.md

show-discovered:
	@sed -n '1,240p' state/discovered_backlog.jsonl
