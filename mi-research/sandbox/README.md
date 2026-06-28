# Sandbox — Experimental Modifications

This directory is for testing modifications to the MI framework
WITHOUT touching the validated core.

## How to Run an Experiment

1. Create a directory: `experiments/your_experiment_name/`
2. Add a `hypothesis.md` explaining what you're testing and why
3. Copy and modify the relevant `mi/` module
4. Run against the 20-case baseline using `scripts/run_retrodiction.py --validate`
5. Document results in `results.md`

## Rules

- **NEVER modify files in `mi/` directly from a sandbox experiment**
- **ALWAYS compare against the baseline before proposing adoption**
- **Document negative results** — they're as valuable as positive ones
- **If improvement with no degradation:** move to `proposed/` and flag for review
- **If any degradation on existing cases:** reject, document why, keep in `experiments/`

## Experiment Template

```
experiments/
  my_experiment/
    hypothesis.md      # What you're testing and why
    modified_scoring.py # Your modified code
    results.md         # What happened
    baseline_comparison.json  # LIVE vs your modification on all 20 cases
```
