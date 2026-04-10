"""Focused smoke tests for the SJ Interiors app."""

import importlib.util
from pathlib import Path
import sys

from starlette.testclient import TestClient

APP_PATH = Path(__file__).with_name("app.py")
ROOT = APP_PATH.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SPEC = importlib.util.spec_from_file_location("sj_interiors_app", APP_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
app = MODULE.app

client = TestClient(app)


def test_main_pages_render() -> None:
    """Core routes should respond successfully."""
    for route in ["/", "/shop", "/about", "/contact", "/health"]:
        response = client.get(route)
        assert response.status_code == 200


def test_home_page_includes_hero_carousel_and_cta() -> None:
    """Home page should expose the carousel-driven hero and key CTA."""
    response = client.get("/")
    html = response.text
    assert "SJ Interiors" in html
    assert 'id="sjHero"' in html
    assert "Shop the Collection" in html
    assert "WhatsApp Us" in html


def test_shop_category_filter_changes_collection() -> None:
    """Shop category query should narrow the content."""
    response = client.get("/shop?category=curtains")
    html = response.text
    assert "Soft Sheer Curtain Pair" in html
    assert "Pleated Blackout Curtain Set" in html
    assert "Signature Stripe Bedsheet Set" not in html


def test_contact_page_shows_contact_paths() -> None:
    """Contact page should keep WhatsApp and social touchpoints visible."""
    response = client.get("/contact")
    html = response.text
    assert "Chat on WhatsApp" in html
    assert "@sj_interior_deco_and_beddings" in html
    assert "08026022672" in html
