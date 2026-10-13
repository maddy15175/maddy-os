# Deploy MADDY OS Web from an Android phone

These steps use GitHub's mobile website and Render. They do not require a PC.

## A. Upload the v2 files to GitHub

1. Download and extract `maddy-os-web-v2.zip` on your phone.
2. Open https://github.com/maddy15175/maddy-os in Chrome and sign in.
3. Open the repository's `main` branch.
4. For each file in the extracted `maddy-os-web-v2` folder, upload it to the matching repository path:
   - Replace `README.md`.
   - Add `Dockerfile` at the repository root.
   - Add `compose.yaml` at the repository root.
   - Add the three files under `docs/`.
5. In GitHub, use **Add file → Create new file** for each file, or use the repository's upload-files flow. Create the `docs` folder by entering a path such as `docs/WEB_OS_ARCHITECTURE.md`.
6. Review the changed file list, enter a commit message such as `Prepare MADDY OS Web v2 deployment`, and commit to `main` only after checking the changes.

The ZIP contains an overlay: keep the existing `app.py`, `index.html`, `requirements.txt`, and `render.yaml`.

## B. Deploy the current web app on Render

1. Open https://dashboard.render.com/.
2. Select **New → Web Service**.
3. Connect `maddy15175/maddy-os`.
4. Choose the free plan if it is offered for your account.
5. Use these settings:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
   - **Health check path:** `/api/health`
6. Click **Create Web Service** and wait for the build to finish.
7. Open the generated `https://...onrender.com` address.

The Dockerfile in this patch is for Docker-capable hosts; the existing `render.yaml` configures Render's Python service. Do not assume Render will boot uploaded ISO files.

## C. Verify

- Open the public URL and confirm the desktop loads.
- Open `/api/health`; it should return JSON with `ok: true`.
- Try `help` in the terminal. It should list the limited demo commands.
- Commands such as `apt`, `bash`, or `python` are not enabled by the current demo terminal.

## D. Do not upload secrets

Never commit `.env` files, passwords, access tokens, private keys, or provider API keys to the repository. Make the repository private if it contains non-public code or data.

## Important limitation

These steps deploy the **dashboard/API prototype only**. They do not enable project execution, a real Linux shell, ISO boot, graphical VM streaming, or persistent user files.
