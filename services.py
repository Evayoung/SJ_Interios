"""Data access helpers for the SJ Interiors website."""

from __future__ import annotations

import logging
from functools import lru_cache
from typing import Any

try:
    from . import content
    from .content import (
        CATEGORIES,
        HERO_SLIDES,
        PRODUCTS,
        SOCIALS,
        VALUE_POINTS,
        WHOLESALE_BENEFITS,
    )
    from .supabase_client import get_public_client, has_supabase
except ImportError:
    import content
    from content import (
        CATEGORIES,
        HERO_SLIDES,
        PRODUCTS,
        SOCIALS,
        VALUE_POINTS,
        WHOLESALE_BENEFITS,
    )
    from supabase_client import get_public_client, has_supabase

try:
    from cachetools import TTLCache, cached
    _brand_config_cache = TTLCache(maxsize=1, ttl=300)
except ImportError:
    def cached(cache):
        def decorator(fn):
            return fn
        return decorator
    _brand_config_cache = {}

logger = logging.getLogger(__name__)


def _value(item: Any, key: str, fallback: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, fallback)
    return getattr(item, key, fallback)


def _normalize_rows(rows: list[Any]) -> list[dict[str, Any]]:
    if rows is None:
        return []
    return [row if isinstance(row, dict) else dict(row) for row in rows]


def _fetch_table(table: str, transform: Any | None = None) -> list[Any]:
    public_client = get_public_client()
    if not public_client:
        return []

    try:
        result = public_client.table(table).select("*").execute()
    except Exception as exc:
        logger.warning("Supabase table fetch failed for %s: %s", table, exc)
        return []

    if getattr(result, "error", None):
        logger.warning("Supabase table fetch error for %s: %s", table, result.error)
        return []

    data = _normalize_rows(getattr(result, "data", []))
    if transform:
        return [transform(item) for item in data]
    return data


@cached(cache=_brand_config_cache)
def get_brand_config() -> dict[str, Any]:
    fallback = {
        "business_name": content.BUSINESS_NAME,
        "business_subtitle": content.BUSINESS_SUBTITLE,
        "tagline": content.TAGLINE,
        "hero_slides": [
            {"image": slide.image, "alt": slide.alt} for slide in HERO_SLIDES
        ],
        "socials": SOCIALS,
        "value_points": VALUE_POINTS,
        "wholesale_benefits": WHOLESALE_BENEFITS,
        "testimonials": content.TESTIMONIALS,
        "transformations": content.TRANSFORMATIONS,
        "whatsapp_number": content.WHATSAPP_NUMBER,
        "phone_numbers": content.PHONE_NUMBERS,
        "address": content.ADDRESS,
    }

    if not has_supabase():
        return fallback

    rows = _fetch_table("brand_config")
    if not rows:
        return fallback

    config: dict[str, Any] = fallback.copy()
    for row in rows:
        key = row.get("key")
        if not key:
            continue
        config[key] = row.get("value", config.get(key))
    return config


def get_testimonials() -> list[dict[str, Any]]:
    """Return dynamic testimonials from approved client_feedback, brand_config, or fallback."""
    live_reviews = []
    if has_supabase():
        try:
            client = get_service_client()
            if client:
                res = client.table("client_feedback").select("*").eq("kind", "review").eq("is_published", True).order("created_at", desc=True).execute()
                rows = getattr(res, "data", [])
                for r in rows:
                    live_reviews.append({
                        "name": r.get("customer_name") or "Valued Client",
                        "role": f"{r.get('location_tag', 'Ilorin')} · {r.get('project_category', 'Interior Furnishing')}",
                        "text": r.get("message", ""),
                    })
        except Exception:
            pass

    if live_reviews:
        return live_reviews

    cfg = get_brand_config()
    return cfg.get("testimonials") or content.TESTIMONIALS


def insert_client_feedback(data: dict[str, Any]) -> dict[str, Any]:
    """Record customer review or service complaint from public storefront."""
    import uuid, time
    fb_id = f"fb-2026-{uuid.uuid4().hex[:6]}"
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    kind = str(data.get("kind") or "review").lower()
    is_rev = kind == "review"

    entry = {
        "id": fb_id,
        "created_at": now_iso,
        "kind": kind,
        "customer_name": str(data.get("customer_name") or "Valued Client").strip(),
        "customer_phone": str(data.get("customer_phone") or "").strip(),
        "customer_email": str(data.get("customer_email") or "").strip(),
        "rating": int(data.get("rating") or 5) if is_rev else 0,
        "project_category": str(data.get("project_category") or "General Interior Furnishing").strip(),
        "location_tag": str(data.get("location_tag") or "Ilorin, Kwara State").strip(),
        "message": str(data.get("message") or "").strip(),
        "order_ref": str(data.get("order_ref") or "").strip(),
        "complaint_type": str(data.get("complaint_type") or ("Review" if is_rev else "General Inquiry")).strip(),
        "urgency": str(data.get("urgency") or "normal").strip(),
        "status": "pending" if is_rev else "open",
        "is_published": False,
        "assigned_to": "",
        "resolution_notes": "",
        "resolved_at": "",
    }

    if has_supabase():
        try:
            client = get_service_client()
            if client:
                client.table("client_feedback").insert(entry).execute()
        except Exception:
            pass

    return entry


def get_transformations() -> list[dict[str, Any]]:
    """Return dynamic before/after transformations from brand_config or fallback."""
    cfg = get_brand_config()
    return cfg.get("transformations") or content.TRANSFORMATIONS


def get_lookbook_items() -> list[dict[str, Any]]:
    """Return dynamic lookbook items or fallback."""
    cfg = get_brand_config()
    return cfg.get("lookbook_items") or [
        {"image": slide.image, "alt": slide.alt} for slide in HERO_SLIDES
    ]


def get_whatsapp_number() -> str:
    """Return active WhatsApp number from brand_config, env, or fallback."""
    try:
        cfg = get_brand_config()
        num = str(cfg.get("whatsapp_number") or "").strip()
        if num:
            return num.replace("+", "").replace(" ", "").replace("-", "")
    except Exception:
        pass
    import os
    return os.getenv("WHATSAPP_NUMBER", content.WHATSAPP_NUMBER).replace("+", "").replace(" ", "").replace("-", "")



def get_categories() -> list[Any]:
    categories = _fetch_table("categories")
    if categories:
        return categories
    return CATEGORIES


def get_products(category_slug: str | None = None, featured_only: bool = False) -> list[Any]:
    products = _fetch_table("products")
    if products:
        if category_slug and category_slug != "all":
            products = [item for item in products if item.get("category_slug") == category_slug]
        if featured_only:
            products = [item for item in products if item.get("is_featured")]
        return products

    if category_slug and category_slug != "all":
        return [product for product in PRODUCTS if product.category == category_slug]
    return PRODUCTS


def get_featured_products(limit: int = 6) -> list[Any]:
    products = get_products(featured_only=True)
    if not products:
        return PRODUCTS[:limit]
    return products[:limit]


def get_services() -> list[dict[str, Any]]:
    services = _fetch_table("services")
    if services:
        return services

    return [
        {
            "title": "Curtain and Blind Styling",
            "slug": "curtain-blind-styling",
            "summary": "Custom curtain and window blind recommendations for every room.",
            "description": "We advise on the right fabrics, patterns, and fittings so your windows feel finished and elegant.",
            "icon": "layout-sidebar-inset",
            "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1400&q=80",
            "is_active": True,
            "sort_order": 1,
        },
        {
            "title": "Bedding and Linen Curation",
            "slug": "bedding-linen-curation",
            "summary": "Soft yet polished bed dressing solutions for homes and guest rooms.",
            "description": "Choose duvet sets, sheet bundles, and accent pillows that work together across rooms.",
            "icon": "stars",
            "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=80",
            "is_active": True,
            "sort_order": 2,
        },
        {
            "title": "Interior Decor Accessories",
            "slug": "decor-accessories",
            "summary": "From cushions to trays, accessories complete a room with layered personality.",
            "description": "We help you choose finishing touches that add depth, texture, and warmth without clutter.",
            "icon": "gem",
            "image": "https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1400&q=80",
            "is_active": True,
            "sort_order": 3,
        },
    ]


def get_category_label(category_slug: str, categories: list[Any] | None = None) -> str:
    categories = categories if categories is not None else get_categories()
    for category in categories:
        label = _value(category, "label")
        slug = _value(category, "slug")
        if slug == category_slug:
            return label
    return "All Collections"


def get_category_slugs() -> list[str]:
    return [_value(category, "slug") for category in get_categories() if _value(category, "slug")]


def get_service_by_slug(slug: str) -> dict[str, Any] | None:
    """Return a single service by its slug."""
    services = get_services()
    for svc in services:
        if _value(svc, "slug") == slug:
            return svc
    return None


def get_product_by_slug(slug: str) -> Any | None:
    """Return a single product by its slug."""
    products = get_products()
    for prod in products:
        if _value(prod, "slug") == slug:
            return prod
    return None


def insert_inquiry(
    customer_name: str,
    phone: str,
    email: str,
    message: str,
    source: str = "contact_form",
    product_id: str | None = None,
    selected_services: list[str] | None = None,
    service_inquiry: bool = False,
) -> dict[str, Any] | None:
    """Insert a customer inquiry into Supabase. Returns the inserted row or None."""
    from supabase_client import get_service_client, has_service_key

    if not has_service_key():
        logger.warning("No service key configured — inquiry not persisted")
        return None

    client = get_service_client()
    if not client:
        return None

    data = {
        "customer_name": customer_name,
        "phone": phone,
        "email": email,
        "message": message,
        "source": source,
        "status": "new",
        "service_inquiry": service_inquiry,
    }
    if product_id:
        data["product_id"] = product_id
    if selected_services:
        data["selected_services"] = selected_services

    try:
        result = client.table("inquiries").insert(data).execute()
        rows = getattr(result, "data", [])
        return rows[0] if rows else None
    except Exception as exc:
        logger.warning("Failed to insert inquiry: %s", exc)
        return None


def insert_whatsapp_click(product_id: str | None = None) -> None:
    """Log a WhatsApp button click as an inquiry."""
    from supabase_client import get_service_client, has_service_key

    if not has_service_key():
        return

    client = get_service_client()
    if not client:
        return

    data = {
        "customer_name": "Anonymous",
        "phone": "",
        "email": "",
        "message": "WhatsApp button clicked",
        "source": "whatsapp",
        "status": "new",
    }
    if product_id:
        data["product_id"] = product_id

    try:
        client.table("inquiries").insert(data).execute()
    except Exception as exc:
        logger.warning("Failed to log WhatsApp click: %s", exc)


def get_order_by_number(order_number: str) -> dict[str, Any] | None:
    """Look up an order by its order number (e.g. SJ-2026-0001)."""
    from supabase_client import get_public_client, has_supabase

    if not has_supabase():
        return None

    client = get_public_client()
    if not client:
        return None

    try:
        result = client.table("orders").select("*").eq("order_number", order_number).execute()
        rows = getattr(result, "data", [])
        return rows[0] if rows else None
    except Exception as exc:
        logger.warning("Failed to fetch order %s: %s", order_number, exc)
        return None


def clear_brand_config_cache() -> None:
    """Invalidate the brand_config cache so fresh data is fetched next call."""
    _brand_config_cache.clear()
