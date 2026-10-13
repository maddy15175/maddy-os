# MADDY Chat — Hugging Face integration patch

This patch adds a `/ai` page with:
- Hugging Face hosted inference via a server-side `/api/hf-chat` route
- Browser fallback using Transformers.js and a small ONNX model
- Mobile-friendly chat UI and clear loading/error states

## Files
- `hf-chat.html`: add to the repository root, next to `app.py` and `index.html`.
- `app.py.route-snippet.txt`: copy the route snippet into `app.py`. It is a snippet, not a replacement for your existing `app.py`.

## Android-friendly GitHub steps
1. Open `https://github.com/maddy15175/maddy-os` in your browser.
2. Upload `hf-chat.html` to the repository root.
3. Edit `app.py`. Add `import requests` near the other imports, then copy the two route functions from `app.py.route-snippet.txt` (remove the comment markers that precede the route definitions). Keep the existing routes intact.
4. Open `requirements.txt` and add this line: `requests>=2.31,<3.0`
5. Edit `index.html` and add a link/button such as `<a href="/ai">Open MADDY Chat AI</a>` in the existing page.
6. Add the card from `index.html.link-snippet.txt` inside the existing `.grid` in `index.html`.
7. Commit changes. If Render is connected to this repository, it should begin a deployment automatically. Check the deployment logs before treating it as live.

## Configure hosted inference (optional)
1. Create a Hugging Face access token with the minimum permissions required at `https://huggingface.co/settings/tokens`.
2. In Render dashboard → your service → Environment, add:
   - `HF_TOKEN` = your Hugging Face token (secret)
   - `HF_MODEL` = a chat-completion model your account can access, for example `Qwen/Qwen2.5-7B-Instruct`
3. Save and redeploy. Never place `HF_TOKEN` in `index.html`, `hf-chat.html`, GitHub, or any public client-side setting.
4. If the chosen model is not available through your account's Inference Providers, choose a supported model. Hosted inference may require credits or paid access.

## Free-first behavior and limitations
- Browser mode does not need a Hugging Face token, but it downloads a model to the user's device. First load may be slow and it may fail on low-memory phones or browsers without sufficient support.
- Hosted mode requires a working token and model access; do not assume it is free or unlimited.
- The browser fallback is best-effort. Check the model card and test the selected ONNX model in your target mobile browser.
- This patch is a starting integration, not a verified production deployment. Add authentication, rate limiting, CSRF protections where relevant, and abuse controls before exposing hosted inference publicly.
