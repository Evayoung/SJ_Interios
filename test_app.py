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


def test_services_page_renders() -> None:
    """Services page should render with service cards."""
    response = client.get("/services")
    html = response.text
    assert response.status_code == 200
    assert "Our Services" in html
    assert "Service" in html  # At least the word appears


def test_order_lookup_page_renders() -> None:
    """Order lookup page should render with form."""
    response = client.get("/order-lookup")
    html = response.text
    assert response.status_code == 200
    assert "Order Status" in html
    assert "order-number" in html


def test_health_endpoint_returns_json() -> None:
    """Health endpoint should return JSON status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "sj-interiors"


def test_shop_htmx_filter_returns_fragment() -> None:
    """HTMX filter endpoint should return product grid fragment."""
    response = client.get("/shop/filter?category=curtains")
    html = response.text
    assert response.status_code == 200
    assert "Soft Sheer Curtain Pair" in html
    assert "Pleated Blackout Curtain Set" in html


def test_shop_htmx_search_returns_results() -> None:
    """HTMX search endpoint should return filtered products."""
    response = client.get("/shop/search?q=duvet")
    html = response.text
    assert response.status_code == 200
    assert "Duvet" in html


def test_contact_form_validation() -> None:
    """Contact form should validate inputs."""
    # Empty submission should fail validation
    response = client.post("/contact/submit", data={"name": "", "phone": "", "email": "", "message": ""})
    assert response.status_code == 200
    assert "alert-danger" in response.text

    # Valid submission
    response = client.post("/contact/submit", data={
        "name": "Test User",
        "phone": "08026022672",
        "email": "test@example.com",
        "message": "I would like to enquire about curtains.",
    })
    assert response.status_code == 200
    assert "alert-success" in response.text or "alert-info" in response.text


def test_shop_product_modal_endpoint() -> None:
    """Quick view modal endpoint should return product fragment."""
    response = client.get("/shop/product-modal/soft-sheer-curtain-pair")
    assert response.status_code == 200
    html = response.text
    assert "Soft Sheer Curtain Pair" in html
    assert "Add to WhatsApp Bag" in html
    assert "Direct 1-Click Order" in html


def test_shop_results_sort_and_search() -> None:
    """Shop results endpoint should filter, search, and sort."""
    response = client.get("/shop/results?category=bedding&sort=price_asc&q=bedsheet")
    assert response.status_code == 200
    html = response.text
    assert "Bedsheet" in html


def test_home_page_renders_transformations_and_testimonials() -> None:
    """Home page should include space transformations and client reviews."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "Space Transformations" in html
    assert "Client Love" in html
    assert "quoteBagOffcanvas" in html
    assert "quickViewModal" in html


def test_order_lookup_empty_state() -> None:
    """Order lookup with invalid number should show not found."""
    response = client.get("/order-lookup/result?order_number=SJ-0000-9999")
    html = response.text
    assert response.status_code == 200
    assert "not found" in html.lower() or "No order found" in html
