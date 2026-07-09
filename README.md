ing # 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

Prerequisite: install `uv` if you don't already have it.

```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

1. Sync the dependencies

   ```
   $ uv sync
   ```

2. Run the app

   ```
   $ uv run streamlit run streamlit_app.py
   ```

### Deploying to Streamlit Community Cloud

1. Push this repository to GitHub.
2. On Streamlit Community Cloud (https://share.streamlit.io) create a new app and connect your GitHub repo.
3. Set the main file to `streamlit_app.py` and the branch to `main` (or your chosen branch).
4. Streamlit will install packages from `requirements.txt` and launch the app. Your live URL will be provided by Streamlit (for example: https://<your-app>.streamlit.app).

If you want the app available at a custom subdomain like `dhammaranking.streamlit.app`, configure the app name/slug in Streamlit settings when you create the app.
