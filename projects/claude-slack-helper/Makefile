PY := .venv/bin/python

setup:            ## create the venv and install dependencies
	python3 -m venv .venv && $(PY) -m pip install -q -r requirements.txt
	@command -v claude >/dev/null || echo "WARNING: 'claude' not on PATH; install Claude Code or use BRAIN=api"

test:             ## unit tests, no model calls, ~1 s
	$(PY) -m pytest -q

evals:            ## 12 real questions through the brain, writes evals/last_run.md (12 model calls)
	$(PY) evals/run_evals.py

demo:             ## record demo/transcript.{md,json} from 6 real cli.py runs
	$(PY) demo/record.py

ask:              ## make ask Q="How many PTO days do I get?"
	$(PY) cli.py "$(Q)"

slack:            ## run the Slack bot (needs SLACK_BOT_TOKEN, SLACK_APP_TOKEN)
	$(PY) -m helper.slack_app

.PHONY: setup test evals demo ask slack
