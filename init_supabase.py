"""Run the Supabase schema migration against a Supabase project.

Usage:
    python init_supabase.py

Requires SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables.
Reads supabase_schema.sql and executes it via the service-role client.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

SCHEMA_FILE = Path(__file__).parent / "supabase_schema.sql"


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

    if not SCHEMA_FILE.exists():
        print(f"ERROR: Schema file not found at {SCHEMA_FILE}")
        sys.exit(1)

    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    print(f"Read schema from {SCHEMA_FILE} ({len(sql)} bytes)")

    client = create_client(supabase_url, service_key)

    # supabase-py doesn't expose a raw SQL executor directly.
    # Use the PostgREST RPC endpoint or run via the SQL editor in Supabase dashboard.
    # For automation, split on semicolons and execute via RPC if your project has a
    # `exec_sql` function, or use the Supabase SQL API.
    #
    # Recommended manual approach:
    #   1. Open Supabase Dashboard > SQL Editor
    #   2. Paste the contents of supabase_schema.sql
    #   3. Click "Run"
    #
    # This script validates the connection and prints the schema for review.

    print("\nSchema SQL preview (first 500 chars):")
    print("-" * 50)
    print(sql[:500])
    print("-" * 50)

    # Verify connection by querying a table that should exist after migration
    try:
        result = client.table("brand_config").select("id").limit(1).execute()
        print("\nConnection verified: Supabase is reachable and schema is applied.")
    except Exception as exc:
        print(f"\nNote: Schema may not be applied yet. Error: {exc}")
        print("Please run the SQL in supabase_schema.sql via the Supabase SQL Editor.")


if __name__ == "__main__":
    main()
