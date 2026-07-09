# SJ Interiors Refurbishment Plan

## Scope Boundaries

- **Public-facing only**: Serves customers exploring SJ Interiors products/services. Admin is a separate app -- not included here.
- **No payments**: WhatsApp-based ordering remains the checkout mechanism.
- **Lightweight order flow**: Inquiries tracked in Supabase, convertible to orders with status (Processing/Shipped/Delivered) and basic sales metrics -- no payment processing.
- **Supabase everything**: Products, categories, services, inquiries, orders, and brand config all live in Supabase.
- **Vercel deployment**: Update app for Vercel + Supabase.
- **Supabase Storage ready**: Architect image infrastructure but start with placeholders.

---

## Task 1: Project Foundation & Environment

### 1.1 -- Create `.env.example` and environment config
- File: `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\.env.example`
- Required vars: `SUPABASE_URL`, `SUPABASE_KEY` (anon public), `SUPABASE_SERVICE_KEY`, `SECRET_KEY`, `WHATSAPP_NUMBER`, `VERCEL`
- Move hardcoded `secret_key` in `app.py` to `os.getenv("SECRET_KEY")`
- Move `WHATSAPP_NUMBER` from `content.py` to env var
- Update `requirements.txt`: add `supabase-py>=2.0`, `python-dotenv`

### 1.2 -- Create Supabase client module
- File: `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\supabase_client.py`
- Singleton client factory using `create_client()` or similar
- Read `SUPABASE_URL` and `SUPABASE_KEY` from env
- Use `anon` key for public-facing queries (RLS-protected), `service_key` for backend operations
- Graceful fallback if env vars missing (support local dev without Supabase)

### 1.3 -- Define Supabase table schemas
- SQL migrations in `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\supabase_schema.sql`

Tables:
- **categories**: id (uuid PK), slug (unique), label, description, icon, image_url, sort_order, is_active, created_at, updated_at
- **products**: id (uuid PK), name, slug (unique), category_id (FK), description, price, highlight, image_url, images (jsonb[] for gallery), stock_status (enum: in_stock/made_to_order/discontinued), is_featured, is_active, created_at, updated_at
- **services**: id (uuid PK), title, slug (unique), summary (short description), description (full HTML/markdown), icon, image_url, is_active, sort_order, created_at, updated_at
- **inquiries**: id (uuid PK), product_id (FK nullable), service_inquiry (boolean default false), customer_name, phone, email, message, source (enum: whatsapp/contact_form/phone/services_page), selected_services (jsonb[] nullable -- list of service slugs/IDs), status (enum: new/contacted/ordered/closed), created_at
- **orders**: id (uuid PK), inquiry_id (FK), order_number (generated, e.g. SJ-2026-0001), customer_name, phone, items (jsonb), status (enum: processing/shipped/delivered/cancelled), notes, created_at, updated_at
- **brand_config**: id (uuid PK), key (unique), value (jsonb) -- for brand name, tagline, address, socials, hero slides, value points, wholesale benefits, etc.

---

## Task 2: Replace Static Content with Supabase Data

### 2.1 -- Create data access layer
- File: `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\services.py`
- Functions:
  - `get_brand_config()` -- Fetch brand config as dict (cached per session)
  - `get_categories()` -- Fetch active categories ordered by sort_order
  - `get_category_by_slug(slug)` -- Single category lookup
  - `get_products(category_slug=None, featured_only=False)` -- Products with optional filters
  - `get_product_by_slug(slug)` -- Single product
  - `get_featured_products(limit=6)` -- For home page preview
  - `get_services()` -- Fetch active services ordered by sort_order
  - `get_service_by_slug(slug)` -- Single service detail
- Graceful degradation: if Supabase unavailable, return empty lists with logged warning -- don't crash

### 2.2 -- Refactor `content.py`
- Repurpose as brand config cache layer
- Remove hardcoded `PRODUCTS`, `CATEGORIES`, `HERO_SLIDES` lists
- Load brand info from Supabase `brand_config` table on first access
- Hero slides, social links, value points, wholesale benefits loaded from brand_config JSON

### 2.3 -- Refactor `components.py`
- Change all component functions to accept data via parameters (they already mostly do)
- `hero_section()`: Accept hero_slides as parameter, remove hardcoded data dependency
- `category_card()` and `featured_categories_section()`: Accept categories list
- `product_card()` and `product_grid()`: Accept products list
- `home_preview_section()`: Accept products parameter
- New: `service_card()` -- card for displaying a single service
- New: `services_grid()` -- responsive grid of service cards with selection checkboxes
- New: `service_inquiry_form()` -- form with multi-select service checkboxes, customer name, phone, message
- Remove import-time data dependency -- components receive data, not import it

### 2.4 -- Refactor `routes.py`
- Each route handler fetches data from `services.py` instead of importing from `content.py`
- `home()`: Fetch brand_config, categories, featured_products, hero_slides, services from Supabase
- `shop()`: Fetch products filtered by category from Supabase
- `about()`: Fetch brand_config, value_points from Supabase
- `contact()`: Fetch brand_config, socials from Supabase
- Remove hardcoded data imports
- Add request-scoped error handling: if Supabase fails, show degraded UI with warning Alert

---

## Task 3: Services Page -- Full Service Catalog with Inquiry Selection

### 3.1 -- Create services route
- New file or new section in `routes.py`
- Route `GET /services` -- full services listing page
- Fetches all active services from Supabase `services` table
- Displays each service in a detailed card with: icon, title, summary, full description, image
- Services represent offerings like: Full House Curtain Design, Complete Interior Decoration, Furniture Supply (mattresses, beds, chairs, vases, tables), Interior Consultancy, etc.

### 3.2 -- Service selection and inquiry flow
- Each service card has a checkbox or "Add to Request" toggle
- A floating or sticky "Request Selected Services" panel shows count of selected services
- On submit, opens inquiry form (or inline section) with:
  - Pre-populated list of selected services
  - Customer name, phone, email, message fields
  - Option to add additional notes
- Form submits via `hx_post="/services/inquiry"` with HTMX toast feedback
- Stores in Supabase `inquiries` table with:
  - `source='services_page'`
  - `selected_services` as JSONB array of service slugs
  - `service_inquiry=true`
- HTMX-powered: checkboxes toggle selection via `hx-post="/services/toggle-selection"`, no page reload

### 3.3 -- Dynamic service content
- The services page renders entirely from Supabase data
- No hardcoded service descriptions in Python
- Admin (future separate app) can add/edit/delete services via the `services` table
- The public page automatically reflects changes without code deployment

---

## Task 4: HTMX Interactivity Upgrade

### 4.1 -- HTMX-powered category filtering (shop page)
- Replace full-page-reload category filter with HTMX partial swap
- `shop_filter_bar()` returns links using `hx_get="/shop/filter?category=X"`, `hx_target="#product-results"`, `hx_push_url="true"`
- New endpoint: `@app.get("/shop/filter")` returns just the product grid HTML fragment
- Product grid wrapper gets `id="product-results"` for swap target
- Add `hx-indicator="#loading-spinner"` for loading state during filter

### 4.2 -- Lazy-loaded sections
- `lookbook_section()` on home page: Use `LazyLoad` preset from Faststrap
- Expensive secondary content loads after page render

### 4.3 -- Live search for products
- Add search input above product grid on shop page
- `ActiveSearch` preset from Faststrap: `hx_get="/shop/search"`, debounce 300ms
- Endpoint returns filtered product grid fragment
- Empty state shown when no results match

### 4.4 -- Contact form with HTMX validation
- Simple form: name, phone, email, message
- `FormGroup` with HTMX blur validation on email/phone
- Submit via `hx_post="/contact/submit"` with toast feedback
- Stores inquiry in Supabase `inquiries` table
- Show success message with `Alert` instead of page reload

---

## Task 5: Lightweight Order & Inquiry Tracking (No Payments)

### 5.1 -- WhatsApp-click inquiry logging
- Each "Order on WhatsApp" button fires `hx_post="/track/whatsapp-click"` (logging silently on click)
- New endpoint logs to Supabase `inquiries` table: product_id, source='whatsapp', timestamp
- Customer sees the normal WhatsApp redirect (HTMX call fires in parallel)
- Use `hx-trigger="click"` with `hx-target` pointing to a hidden div

### 5.2 -- Public order lookup page
- New route: `/order-lookup` -- simple form with order number input
- On submit, fetches order from Supabase `orders` table by order_number
- Shows order status, items, timeline (Processing -> Shipped -> Delivered with dates)
- Shows "Order not found" empty state for invalid numbers
- Link to this page in footer

### 5.3 -- Product inquiry form per product
- On each product card, optional "Request Quote" button alongside WhatsApp
- Opens a Faststrap `Modal` with a simple form (name, phone, message)
- On submit, creates inquiry in Supabase linked to the product
- HTMX-driven modal with form validation

---

## Task 6: CSS Architecture & Visual Polish (Faststrap Standards)

### 6.1 -- Split CSS into modular files
- Create: `assets/css/_brand.css` -- CSS custom properties, brand tokens, semantic colors
- Create: `assets/css/_typography.css` -- hero-title, section-title, body, label classes
- Create: `assets/css/_layout.css` -- section spacing, shell, stacks, site-nav
- Create: `assets/css/_surfaces.css` -- cards, panels, glass, borders, shadows
- Create: `assets/css/_interactions.css` -- buttons, hover states, transitions, focus
- Update: `custom.css` -- imports all the above via `@import url(...)`

### 6.2 -- Remove Bootstrap-smell violations
- Change `border-radius: 999px` on nav-links to 4px-6px
- Change `border-radius: 999px` on filter-pills to 5px
- Change `border-radius: 999px` on product-btn to 5px
- Change `border-radius: 2rem` on hero-shell to 1rem
- Remove `!important` flags where possible by increasing selector specificity
- Remove `shadow-sm` from site-nav (too default-Bootstrap)
- Replace `Badge(pill=True)` default with `pill=False` or override radius in CSS

### 6.3 -- Add Fx animations
- Apply `Fx.fade_in` to section heroes and feature cards
- Apply `Fx.hover_lift` to product and category cards
- Apply `Fx.stagger` to grid items for staggered entrance
- Leverage Faststrap's `Fx` class from `core/effects.py`

### 6.4 -- Add dark mode CSS
- Add `[data-bs-theme="dark"]` counterparts for all surface, text, and border tokens in `_brand.css`
- Add `ThemeToggle` component in navbar or footer
- Test both modes for contrast and legibility

---

## Task 7: Supabase Storage & Image Infrastructure

### 7.1 -- Configure Supabase storage bucket
- SQL migration to create `product-images` bucket
- RLS policy: public read access, authenticated write access
- Image URL format: `https://{project}.supabase.co/storage/v1/object/public/product-images/{product_slug}/{filename}`

### 7.2 -- Image helper utilities
- Function: `get_product_image_url(product_slug, filename, fallback_url)` -- builds correct storage URL or falls back to placeholder
- Function: `get_placeholder_url(category_slug)` -- returns SVG placeholder path for category/product without images
- Products store `images` as JSONB array of `{url, alt, is_primary}`

---

## Task 8: Error Handling, States & UX Coverage

### 8.1 -- Custom error pages
- `@app.exception_handler(404)` -- branded 404 page with "Browse Shop" CTA
- `@app.exception_handler(500)` -- branded error page with "Try Again" + "Contact Us" links
- Use `ErrorPage` from Faststrap if available, or custom component

### 8.2 -- Empty and loading states
- Shop: `EmptyState` when no products match filter/search
- Services: `EmptyState` if no services configured yet (graceful for new installs)
- Order lookup: `EmptyState` when order not found
- Contact form: loading spinner on submit via `LoadingButton` or `Spinner`
- Product grid: `PlaceholderCard` while HTMX filter is loading

### 8.3 -- Form validation
- Contact form: `FormGroup` with `FormErrorSummary`
- Phone validation (Nigerian format awareness)
- Email validation via HTMX blur endpoint
- Order lookup: validate order number format before querying

---

## Task 9: Update `app.py` for Vercel + Supabase

### 9.1 -- Production hardening
```python
import os
from fasthtml.common import FastHTML, Link, serve
from faststrap import add_bootstrap, mount_assets
from supabase_client import init_supabase

app = FastHTML(
    secret_key=os.getenv("SECRET_KEY", "dev-fallback-key"),
)

# Initialize Supabase
supabase = init_supabase()

add_bootstrap(app, theme=SJ_INTERIORS_THEME, mode="dark",
              use_cdn=bool(os.getenv("VERCEL")))

# Asset mounting
mount_assets(app, str(Path(__file__).parent / "assets"), url_path="/assets")
```

### 9.2 -- Update `vercel.json`
```json
{
  "builds": [{ "src": "app.py", "use": "@vercel/python" }],
  "rewrites": [{ "source": "/(.*)", "destination": "/app.py" }],
  "headers": [
    { "source": "/assets/(.*)", "headers": [
      { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
    ]}
  ]
}
```

### 9.3 -- Static asset handling on Vercel
- Remove `@vercel/static` build for assets -- let FastHTML's `mount_assets` handle it
- Add long-term cache headers for static assets (CSS, images)
- Ensure SVG placeholders under `assets/` are properly served

---

## Task 10: Testing

### 10.1 -- Update tests
- Update `test_app.py` to work with Supabase-dependent routes (mock Supabase or use test fixtures)
- Add tests for: services page rendering, empty product states, 404 handler, order lookup for missing orders
- Add test for HTMX fragment endpoints returning correct HTML
- Add test for contact form validation
- Add test for service inquiry submission

---

## Task 11: Seed Data & Migration

### 11.1 -- Create seed script
- File: `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\seed_supabase.py`
- Seeds categories, products, services, and brand_config from existing `content.py` data into Supabase
- Seed initial services: Full House Curtain Design, Complete Interior Decoration, Furniture Supply (mattresses/beds/chairs/vases/tables), Interior Consultancy, Window Treatment Solutions, Home Styling & Accessories
- Uploads placeholder SVG images to storage bucket
- One-time run script

### 11.2 -- Create migration/init script
- File: `c:\Users\Meshell\Desktop\FastHTML\sj_interiors\init_supabase.py`
- Reads `supabase_schema.sql` and executes against Supabase
- Creates tables, indexes, RLS policies, storage bucket

---

## Implementation Order

```
Phase A -- Foundation (Tasks 1, 9, 11)
  Task 1.1 -> 1.2 -> 1.3 -> 9.1 -> 9.2 -> 9.3 -> 11.1 -> 11.2

Phase B -- Data Migration (Tasks 2)
  Task 2.1 -> 2.2 -> 2.3 -> 2.4

Phase C -- Services Page (Tasks 3)
  Task 3.1 -> 3.2 -> 3.3

Phase D -- Interactivity (Tasks 4)
  Task 4.1 -> 4.2 -> 4.3 -> 4.4

Phase E -- Order Tracking (Tasks 5)
  Task 5.1 -> 5.2 -> 5.3

Phase F -- Visual & CSS (Tasks 6, 7)
  Task 6.1 -> 6.2 -> 6.3 -> 6.4 -> 7.1 -> 7.2

Phase G -- UX Completion (Tasks 8, 10)
  Task 8.1 -> 8.2 -> 8.3 -> 10.1
```

Each phase builds on the previous and can be verified independently before moving forward.