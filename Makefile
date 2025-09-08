merge-from-sourced:
	@python3 scripts/merge_from_sourced.py
merge-apply:
	@python3 scripts/merge_from_sourced.py --apply

pr-body:
	@python3 scripts/gen_pr_body.py

ssot:
	@python3 scripts/assemble_ssot.py

check:
	@echo 'Basic checks placeholder'

router-test:
	@python3 scripts/router_smoke_test.py

code-lift:
	@python3 scripts/lift_code_blocks.py fix

seed-from-sources:
	@python3 scripts/seed_from_sources.py

ci:
	@python3 scripts/lift_code_blocks.py check
	@python3 scripts/assemble_ssot.py
	@python3 scripts/router_smoke_test.py


    .PHONY: curator-analyze curator-plan curator-apply
    curator-analyze:
	python scripts/curator_agent.py analyze
    curator-plan:
	python scripts/curator_agent.py plan
    curator-apply:
	python scripts/curator_agent.py apply
