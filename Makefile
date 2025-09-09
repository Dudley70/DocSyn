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

.PHONY: merge-from-sourced merge-apply pr-body ssot check router-test code-lift seed-from-sources clean-staging ci docsyn verify qa curator-analyze curator-plan curator-apply gen-curation-index manifest-guard

clean-staging:
	@python3 scripts/clean_staging_duplicates.py --delete --fail-if-leftovers

docsyn: ## Promote staged files and build/validate (source of truth)
	@python3 scripts/promote_updated.py
	@make ci

verify: ## Build and assert compiled hash matches baseline
	@rm -rf dist/
	@make docsyn >/dev/null
	@python3 scripts/verify_baseline.py

qa: manifest-guard ## Run quality assurance checks
	@python3 scripts/qa_build.py

gen-curation-index: ## Generate deterministic curated sources index
	@python3 scripts/tools/gen_curation_index.py --manifest build.manifest.json --root .

manifest-guard: ## Validate manifest integrity and vendor ordering
	@python3 scripts/tools/manifest_guard.py --manifest build.manifest.json --root .

ci: clean-staging
	@python3 scripts/lift_code_blocks.py check
	@python3 scripts/assemble_ssot.py
	@python3 scripts/router_smoke_test.py
	@python3 scripts/qa_build.py

curator-analyze:
	@python3 scripts/curator_agent.py analyze

curator-plan:
	@python3 scripts/curator_agent.py plan

curator-apply:
	@python3 scripts/curator_agent.py apply
