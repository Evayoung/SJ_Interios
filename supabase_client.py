"""Supabase client helper for SJ Interiors."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


@lru_cache(maxsize=1)
def get_public_client():
    """Return a singleton Supabase public client or None if not configured."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(SUPABASE_URL, SUPABASE_KEY)


@lru_cache(maxsize=1)
def get_service_client():
    """Return a singleton Supabase service client or None if not configured."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        return None
    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def has_supabase() -> bool:
    return bool(SUPABASE_URL and SUPABASE_KEY)


def has_service_key() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SERVICE_KEY)
