# MADDY OS starter (Android-friendly deployment)

This starter provides:
- Responsive browser desktop UI
- Flask JSON API and health check
- Safe allowlisted demo terminal commands
- Browser-local demo file manager (localStorage)
- Restricted arithmetic endpoint, not arbitrary Python execution
- Render deployment configuration

## Deploy on Render from Android
1. Create a GitHub repository in your browser and upload these files, keeping `app.py`, `requirements.txt`, and `render.yaml` at the repository root.
2. Open https://dashboard.render.com/ and sign up.
3. Choose **New → Web Service**, connect your repository, and select the **Free** instance.
4. If Render doesn't automatically use `render.yaml`, set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Deploy. Open the generated `https://YOUR-SERVICE.onrender.com` URL.

Render documents its free deployment workflow here:
https://render.com/docs/your-first-deploy

## Important limitations
- This is a starter/prototype, not a complete operating system.
- The terminal intentionally does NOT run arbitrary shell commands.
- `/api/python-math` evaluates only basic arithmetic. Never replace it with `eval`, `exec`, or shell execution using public user input.
- The file manager stores data in the current browser's localStorage, not on the server; clearing browser data deletes it.
- No login system, server-side persistent user storage, full Python interpreter, or QEMU/ISO boot support is included.
- Render free web services may sleep while idle and have an ephemeral filesystem. Use a suitable persistent storage service for important files.
- Before public launch, add authentication, request limits, validation, privacy protections, and isolated execution for any code-running feature.

## Local run (optional)
Python 3.10+:
```bash
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:10000
