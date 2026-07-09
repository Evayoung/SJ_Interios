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

logger = logging.getLogger(__name__)


def _value(item: Any, key: str, fallback: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, fallback)
    return getattr(item, key, fallback)


def _normalize_rows(rows: list[Any]) -> list[dict[str, Any]]:
    if rows is None:
        return []
    return [row if isinstance(row, dict) else dict(row)]


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


@lru_cache(maxsize=1)
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
