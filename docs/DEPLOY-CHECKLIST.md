# Deploy checklist

Before pushing
- [ ] `python scripts/validate_profile.py` reports 0 errors
- [ ] Read `docs/PROFILE-CONTENT.md`; every statement is true today
- [ ] Status labels (In development / Exploratory / Building / Ongoing) are accurate
- [ ] No private details, keys or supplier data in any file

After pushing
- [ ] Settings → Actions → General → Workflow permissions = Read and write
- [ ] Run **Profile 3D contribution graph** and **Contribution snake** manually; both green
- [ ] Branch `output` exists with two SVGs; `profile-3d-contrib/profile-night-view.svg` exists
- [ ] If the 3D workflow failed on "Check the file used by README.md exists", fix the README path
- [ ] **Validate profile** runs green on `main`
- [ ] Open `https://github.com/raa-mm` on desktop: no broken images, no sideways scrolling
- [ ] Open it on a phone and in both light and dark theme; snake switches theme
- [ ] Stats and streak cards load (if not, retry later)
- [ ] Optional: `python scripts/check_external_links.py`
