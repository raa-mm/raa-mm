# Workflows

| Workflow | Trigger | Writes | Output |
| :-- | :-- | :-- | :-- |
| `snake.yml` | daily 02:17 UTC, manual | branch `output` | `github-snake.svg`, `github-snake-dark.svg` |
| `profile-3d.yml` | daily 02:47 UTC, manual | `main` | `profile-3d-contrib/*.svg` (README uses `profile-night-view.svg`) |
| `validate-profile.yml` | push to `main`, pull requests | nothing | pass/fail log |

## snake.yml
Uses `Platane/snk/svg-only@v3` to render the SVGs, then publishes them to the `output` branch with plain git (no third-party publishing action). It creates the branch on first run, skips the commit when nothing changed, and fails with a clear message if an expected file is missing. Permissions: `contents: write`. README reads the files from `raw.githubusercontent.com/raa-mm/raa-mm/output/`.

## profile-3d.yml
Uses `yoshi389111/github-profile-3d-contrib@0.7.1` with `GITHUB_TOKEN` and `USERNAME`. It checks that the file README uses exists, commits only when something changed, rebases before pushing. With the default token only public contributions are counted.

## validate-profile.yml
Runs `scripts/validate_profile.py`: required files, README local references and alt text, SVG validity, workflow structure, username and identity checks, unverified-claim wording. Permissions: `contents: read`.

## Not added
No workflow for stats cards (they are rendered on request by third-party services) and no link-check workflow (flaky by nature; run `scripts/check_external_links.py` by hand).

## Verification status
Action versions and inputs were written from knowledge of their documentation, not re-checked online in the environment that produced this repository. Confirm on first run; see `docs/DEPLOY-CHECKLIST.md`.
