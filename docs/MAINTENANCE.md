# Maintenance

- **Change text**: edit `README.md`, then update `docs/PROFILE-CONTENT.md`.
- **Add a project**: copy `docs/PROJECT-CARD-TEMPLATE.md`, duplicate an existing `assets/project-*.svg`, change the illustration, name, subtitle and status, add the section to the README. Only link repositories and demos you have opened and confirmed.
- **Add a technology**: add a chip (see `assets/README.md`) and use it in the stack table and the relevant project.
- **Update actions**: when Dependabot or a failing run points to a new major version of `Platane/snk`, `yoshi389111/github-profile-3d-contrib`, `actions/checkout` or `actions/setup-python`, change the `uses:` line and run the workflow manually.
- **If a stats card is blank**: the third-party service is rate-limited or down. Wait, or remove the card; nothing else depends on it.
- **If the 3D image breaks**: run the workflow, open the log and compare the generated file names with the path in `README.md`.
- **Before every push**: `python scripts/validate_profile.py`.
- **Secrets**: none are needed. Never paste tokens into workflows.
