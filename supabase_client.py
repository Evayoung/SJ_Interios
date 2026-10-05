"""Supabase client helper for SJ Interiors."""

import os
import re
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


def _normalize_supabase_url(raw_url: str | None) -> str:
    if not raw_url:
        return ""
    url = raw_url.strip()
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        match = re.search(r"postgres(?:ql)?://(?:postgres\.)?([a-z0-9]+):", url)
        if match:
            return f"https://{match.group(1)}.supabase.co"
    return url.rstrip("/")


@lru_cache(maxsize=1)
def get_public_client():
    """Return a singleton Supabase public client or None if not configured."""
    url = _normalize_supabase_url(SUPABASE_URL)
    if not url or not SUPABASE_KEY:
        return None
    try:
        from supabase import create_client
        return create_client(url, SUPABASE_KEY)
    except ImportError:
        return None


@lru_cache(maxsize=1)
def get_service_client():
    """Return a singleton Supabase service client or None if not configured."""
    url = _normalize_supabase_url(SUPABASE_URL)
    if not url or not SUPABASE_SERVICE_KEY:
        return None
    try:
        from supabase import create_client
        return create_client(url, SUPABASE_SERVICE_KEY)
    except ImportError:
        return None


def has_supabase() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def has_service_key() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SERVICE_KEY)
