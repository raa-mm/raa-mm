# Setup and publishing

The repository is meant to be pushed to `https://github.com/raa-mm/raa-mm` (the repo whose name matches your username; its README appears on your profile).

## 1. Check locally (optional but quick)
```bash
pip install pyyaml
python scripts/validate_profile.py
```
Expect 0 errors. One warning about `profile-3d-contrib/` is normal before the first workflow run.

## 2. Push
```bash
git init -b main
git remote add origin https://github.com/raa-mm/raa-mm.git
git add .
git commit -m "feat: new profile"
git push -u origin main --force   # only if you want to replace the existing profile repo contents
```
If the existing repository has work you want to keep, pull it first and merge instead of forcing. Review `docs/DEPLOY-CHECKLIST.md` before pushing.

## 3. Allow workflows to write
Repository **Settings → Actions → General → Workflow permissions**: choose **Read and write permissions**. Also make sure Actions are enabled for the repository.

## 4. Run the generators once
**Actions** tab → run **Profile 3D contribution graph**, then **Contribution snake**, using *Run workflow*. Afterwards the `output` branch and `profile-3d-contrib/` folder exist and the README images appear. They then refresh daily.

## 5. Check your profile
Open `https://github.com/raa-mm` on desktop and on your phone. See `docs/DEPLOY-CHECKLIST.md`.
