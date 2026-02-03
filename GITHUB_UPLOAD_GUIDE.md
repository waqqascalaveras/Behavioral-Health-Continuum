# GitHub Upload Guide

Since this workstation doesn't have Git installed, use the Python-based upload script to push changes to GitHub.

## Repository
**https://github.com/waqqascalaveras/Behavioral-Health-Continuum.git**

## Prerequisites

1. **Install PyGithub** (one-time setup):
   ```powershell
   pip install PyGithub
   ```

2. **Create GitHub Personal Access Token** (one-time setup):
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "Behavioral Health Upload"
   - Select scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
   - Click "Generate token"
   - **Copy the token** (you won't see it again!)
   - Token is cached in `.github_token_cache` (never commit this file!)

## Usage

### First Upload (Initial Setup)
```powershell
python upload_to_github.py
```
- Enter your GitHub token when prompted
- Script will upload all project files to the repository

### Subsequent Uploads (Update Changes)
```powershell
python upload_to_github.py
```
- Uses cached token (no prompt)
- Only uploads changed files (smart hash-based detection)
- Much faster than first upload

### Options

**Dry Run (Preview Changes):**
```powershell
python upload_to_github.py --dry-run
```
- Shows what would be uploaded
- Doesn't actually upload anything
- Good for testing before real upload

**Force Re-upload All Files:**
```powershell
python upload_to_github.py --force
```
- Ignores file hash cache
- Re-uploads everything
- Use if files are corrupted on GitHub

**Verbose Mode (Detailed Logs):**
```powershell
python upload_to_github.py --verbose
```
- Shows detailed progress
- Useful for debugging
- Logs saved to `github_upload.log`

**Clear Caches:**
```powershell
python upload_to_github.py --clean
```
- Removes token cache
- Removes file hash cache
- Next run will prompt for token again

**Help:**
```powershell
python upload_to_github.py --help
```

## What Gets Uploaded

**Included:**
- All Python files (`.py`)
- Configuration files (`config.py`, `.gitignore`)
- Documentation (`.md` files)
- Dashboard code (`dashboards.py`)
- ETL pipeline (`etl/` folder)
- Launcher scripts

**Excluded (automatically skipped):**
- Output data files (`output_csv/`, `*.sqlite`, `*.xlsx`)
- Downloaded data (`etl/downloads/`)
- Log files (`*.log`, `etl.log`)
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.venv/`)
- Token cache (`.github_token_cache`)
- OS files (`.DS_Store`, `Thumbs.db`)

See `.gitignore` for the complete exclusion list.

## Troubleshooting

**"PyGithub not installed"**
```powershell
pip install PyGithub
```

**"Authentication failed"**
- Token may be expired or invalid
- Run with `--clean` to clear cached token
- Generate new token at https://github.com/settings/tokens
- Ensure token has `repo` and `workflow` scopes

**"Repository not found"**
- Verify you have access to: https://github.com/waqqascalaveras/Behavioral-Health-Continuum
- Check repository name spelling
- Ensure repository exists

**SSL Verification Errors**
```powershell
python upload_to_github.py --insecure
```
⚠️ Only use if on network with SSL inspection

**Large Upload Times**
- First upload may take several minutes
- Subsequent uploads are much faster (only changed files)
- Use `--dry-run` to see what will be uploaded
- Consider excluding large data files (already done via `.gitignore`)

## Security Notes

- ⚠️ **Never commit `.github_token_cache`** — This file is in `.gitignore`
- 🔐 Token has full repo access — Keep it secure
- 🗑️ Delete token cache file if sharing this folder: `Remove-Item .github_token_cache`
- 🔄 Revoke tokens you're no longer using at: https://github.com/settings/tokens

## Workflow Example

```powershell
# 1. Make changes to code
# (edit files in VS Code)

# 2. Preview what will be uploaded
python upload_to_github.py --dry-run

# 3. Upload changes to GitHub
python upload_to_github.py

# 4. Verify on GitHub
# Visit: https://github.com/waqqascalaveras/Behavioral-Health-Continuum
```

## Advanced: Combining with Other Commands

**Upload after ETL run:**
```powershell
python run_etl.py
python upload_to_github.py
```

**Force upload with verbose logging:**
```powershell
python upload_to_github.py --force --verbose
```

---
For more details, see the script itself: [upload_to_github.py](upload_to_github.py)
