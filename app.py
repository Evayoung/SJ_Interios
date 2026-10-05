"""FastHTML app entrypoint for the SJ Interiors website."""

import os
from pathlib import Path

from fasthtml.common import FastHTML, Link, serve

from faststrap import add_bootstrap, mount_assets

try:
    from .routes import setup_site_routes
    from .theme import SJ_INTERIORS_THEME, setup_sj_interiors_defaults
except ImportError:
    from routes import setup_site_routes
    from theme import SJ_INTERIORS_THEME, setup_sj_interiors_defaults

app = FastHTML(
    secret_key=os.getenv("SECRET_KEY", "sj-interiors-secret"),
    session_cookie="sj_interiors_session",
)

add_bootstrap(
    app,
    theme=SJ_INTERIORS_THEME,
    mode="light",
    use_cdn=bool(os.getenv("VERCEL")),
    font_family='"Trebuchet MS", "Segoe UI", "Aptos", sans-serif',
)

setup_sj_interiors_defaults()

# On Vercel, vercel.json ships the local assets/ directory as static files.
# Keep local asset mounting for local runs.
Environment=os.getenv('VERCEL')
try:
    if not Environment or Environment == "False":
        BASE_DIR = Path(__file__).resolve().parent
        mount_assets(app, str(BASE_DIR / "assets"), url_path="/assets")
except Exception as e:
    print(f"Error mounting local assets: {e}")

app.hdrs = app.hdrs + [
    Link(rel="stylesheet", href="/assets/custom.css?v=20260724"),
]

setup_site_routes(app)


if __name__ == "__main__":
    serve(port=5057)
