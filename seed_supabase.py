"""Seed the Supabase database with initial SJ Interiors data.

Usage:
    python seed_supabase.py

Requires SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables.
Idempotent: skips rows whose slug/key already exists.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Add project root to path for content imports
sys.path.insert(0, str(Path(__file__).parent))

from content import (
    CATEGORIES,
    HERO_SLIDES,
    PHONE_NUMBERS,
    PRODUCTS,
    SOCIALS,
    VALUE_POINTS,
    WHATSAPP_NUMBER,
    WHOLESALE_BENEFITS,
    BUSINESS_NAME,
    BUSINESS_SUBTITLE,
    TAGLINE,
    SHORT_INTRO,
    ADDRESS,
    LOCATION_SHORT,
)


def _upsert_row(client, table: str, data: dict, conflict_col: str | None = None) -> bool:
    """Insert a row, skipping if it already exists (by conflict column)."""
    try:
        if conflict_col:
            # Check if row exists first (simple idempotency)
            existing = client.table(table).select(conflict_col).eq(conflict_col, data[conflict_col]).execute()
            if existing.data:
                return False
        client.table(table).insert(data).execute()
        return True
    except Exception as exc:
        print(f"  Warning: {table} insert failed for {data.get(conflict_col, '?')}: {exc}")
        return False


def seed_categories(client) -> None:
    print("\nSeeding categories...")
    for i, cat in enumerate(CATEGORIES):
        data = {
            "slug": cat.slug,
            "label": cat.label,
            "description": cat.description,
            "icon": cat.icon,
            "image_url": cat.image,
            "sort_order": i,
            "is_active": True,
        }
        if _upsert_row(client, "categories", data, "slug"):
            print(f"  + {cat.label}")
        else:
            print(f"  = {cat.label} (exists)")


def seed_products(client) -> None:
    print("\nSeeding products...")
    for prod in PRODUCTS:
        data = {
            "name": prod.name,
            "slug": prod.name.lower().replace(" ", "-").replace("&", "and"),
            "category_slug": prod.category,
            "description": prod.description,
            "price": prod.price,
            "highlight": prod.highlight,
            "image_url": prod.image,
            "images": [],
            "stock_status": "in_stock",
            "is_featured": True,
            "is_active": True,
        }
        if _upsert_row(client, "products", data, "slug"):
            print(f"  + {prod.name}")
        else:
            print(f"  = {prod.name} (exists)")


def seed_services(client) -> None:
    print("\nSeeding services...")
    services = [
        {
            "title": "Full House Curtain Design",
            "slug": "full-house-curtain-design",
            "summary": "Complete curtain solutions for every room in your home.",
            "description": "From consultation to installation, we design and supply curtains that transform your entire house. We handle measurements, fabric selection, and styling for bedrooms, living rooms, dining areas, and more.",
            "icon": "layout-sidebar-inset",
            "image_url": HERO_SLIDES[1].image,
            "sort_order": 1,
        },
        {
            "title": "Complete Interior Decoration",
            "slug": "complete-interior-decoration",
            "summary": "End-to-end interior styling for homes and commercial spaces.",
            "description": "Our team helps you create a cohesive look across your space — from curtains and blinds to bedding, pillows, and decorative accessories. We handle the full design concept so you don't have to.",
            "icon": "palette",
            "image_url": HERO_SLIDES[3].image,
            "sort_order": 2,
        },
        {
            "title": "Furniture Supply",
            "slug": "furniture-supply",
            "summary": "Quality mattresses, beds, chairs, vases, and tables.",
            "description": "We supply a curated selection of furniture including mattresses, bed frames, accent chairs, decorative vases, and tables. All pieces are selected for comfort, durability, and style.",
            "icon": "armchair",
            "image_url": HERO_SLIDES[0].image,
            "sort_order": 3,
        },
        {
            "title": "Interior Consultancy",
            "slug": "interior-consultancy",
            "summary": "Expert advice for your interior design projects.",
            "description": "Not sure where to start? Our consultancy service provides professional guidance on color schemes, fabric choices, furniture placement, and overall room styling. Available for homes, offices, and hospitality spaces.",
            "icon": "lightbulb",
            "image_url": HERO_SLIDES[2].image,
            "sort_order": 4,
        },
        {
            "title": "Window Treatment Solutions",
            "slug": "window-treatment-solutions",
            "summary": "Blinds, shades, and curtains for every window type.",
            "description": "We specialize in window treatments including venetian blinds, roller blinds, sheer curtains, blackout curtains, and custom solutions. Perfect for homes, offices, and hotels.",
            "icon": "window",
            "image_url": CATEGORIES[4].image if len(CATEGORIES) > 4 else HERO_SLIDES[1].image,
            "sort_order": 5,
        },
        {
            "title": "Home Styling & Accessories",
            "slug": "home-styling-accessories",
            "summary": "Finishing touches that complete your interior look.",
            "description": "From throw pillows and decorative trays to mirrors and accent pieces, we help you find the perfect accessories to finish your rooms. Small details make a big difference.",
            "icon": "gem",
            "image_url": CATEGORIES[5].image if len(CATEGORIES) > 5 else HERO_SLIDES[3].image,
            "sort_order": 6,
        },
    ]

    for svc in services:
        data = {
            **svc,
            "is_active": True,
        }
        if _upsert_row(client, "services", data, "slug"):
            print(f"  + {svc['title']}")
        else:
            print(f"  = {svc['title']} (exists)")


def seed_brand_config(client) -> None:
    print("\nSeeding brand_config...")
    configs = [
        ("business_name", BUSINESS_NAME),
        ("business_subtitle", BUSINESS_SUBTITLE),
        ("tagline", TAGLINE),
        ("short_intro", SHORT_INTRO),
        ("whatsapp_number", WHATSAPP_NUMBER),
        ("phone_numbers", PHONE_NUMBERS),
        ("address", ADDRESS),
        ("location_short", LOCATION_SHORT),
        ("hero_slides", [{"image": s.image, "alt": s.alt} for s in HERO_SLIDES]),
        ("socials", SOCIALS),
        ("value_points", [{"title": t, "copy": c} for t, c in VALUE_POINTS]),
        ("wholesale_benefits", WHOLESALE_BENEFITS),
        ("testimonials", content.TESTIMONIALS),
        ("transformations", content.TRANSFORMATIONS),
    ]

    for key, value in configs:
        data = {"key": key, "value": value}
        if _upsert_row(client, "brand_config", data, "key"):
            print(f"  + {key}")
        else:
            print(f"  = {key} (exists)")



def main() -> None:
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")

    if not supabase_url or not service_key:
        print("ERROR: Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env first.")
        sys.exit(1)

    try:
        from supabase import create_client
    except ImportError:
        print("ERROR: Install supabase-py first: pip install supabase-py>=2.0")
        sys.exit(1)

    print(f"Connecting to Supabase...")
    client = create_client(supabase_url, service_key)

    seed_categories(client)
    seed_products(client)
    seed_services(client)
    seed_brand_config(client)

    print("\nSeed complete!")


if __name__ == "__main__":
    main()
