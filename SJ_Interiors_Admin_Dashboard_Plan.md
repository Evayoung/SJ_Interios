# SJ Interiors Admin Dashboard — Detailed Implementation Plan

## Executive Summary

Build a fully-branded, PWA-capable admin dashboard for SJ Interiors that manages all public website content and provides business tools (proposals, quotations, invoices). The admin follows the proven neo-admin architecture: FastHTML + Faststrap + Supabase + HTMX, with a dark-first glassmorphism design system matching the SJ Interiors purple/gold brand.

**Separate app** at `C:\Users\Meshell\Desktop\FastHTML\sj_admin` (sibling to `sj_interiors`).

---

## 1. Project Structure

```
sj_admin/
├── main.py                          # Entrypoint (serve)
├── conftest.py                      # Pytest fixtures
├── test_app.py                      # Smoke tests
├── requirements.txt                 # Dependencies
├── vercel.json                      # Vercel deployment
├── .env / .env.example              # Environment variables
├── .gitignore / .vercelignore
├── sync_supabase_schema.py          # Schema sync script
│
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastHTML app shell
│   ├── config.py                    # Settings dataclass
│   ├── theme.py                     # Faststrap theme + defaults
│   ├── schema.py                    # Declarative CRUD config (Field + TableConfig)
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   └── models.py                # Frozen dataclasses for all entities
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── supabase_client.py       # Service-role client singleton
│   │   ├── auth_repository.py       # Login/auth logic
│   │   ├── category_repository.py   # CRUD for categories
│   │   ├── product_repository.py    # CRUD for products
│   │   ├── service_repository.py    # CRUD for services
│   │   ├── inquiry_repository.py    # Inquiries + status management
│   │   ├── order_repository.py      # Orders + status tracking
│   │   ├── brand_repository.py      # Brand config CRUD
│   │   ├── media_repository.py      # Supabase Storage uploads
│   │   ├── document_repository.py   # Proposals, quotations, invoices
│   │   ├── document_pdf.py          # PDF generation (ReportLab)
│   │   └── sql/
│   │       ├── 001_admin_schema.sql # New tables: admin_users, documents, document_items
│   │       └── 002_admin_rls.sql    # Admin RLS policies
│   │
│   ├── routes/
│   │   ├── __init__.py              # setup_routes(app)
│   │   ├── auth.py                  # /login, /logout
│   │   ├── dashboard.py             # /, /dashboard/metrics
│   │   ├── categories.py            # /categories, /categories/save
│   │   ├── products.py              # /products, /products/save, /products/upload-image
│   │   ├── services.py              # /services, /services/save
│   │   ├── inquiries.py             # /inquiries, /inquiries/save
│   │   ├── orders.py                # /orders, /orders/save
│   │   ├── documents.py             # /documents (proposals/quotes/invoices)
│   │   ├── media.py                 # /media, /media/upload
│   │   └── settings.py              # /settings, /settings/save
│   │
│   └── presentation/
│       ├── __init__.py
│       ├── shell.py                 # page_frame(), sidebar, bottom nav, mobile drawer
│       ├── page_helpers.py          # Shared form widgets
│       └── pages/
│           ├── __init__.py
│           ├── auth.py              # Login page
│           ├── dashboard.py         # Overview with metrics
│           ├── categories.py        # Category list/editor
│           ├── products.py          # Product list/editor
│           ├── services.py          # Service list/editor
│           ├── inquiries.py         # Inquiry inbox
│           ├── orders.py            # Order pipeline
│           ├── documents.py         # Document workspace (proposals/quotes/invoices)
│           ├── media.py             # Media library
│           └── settings.py          # Brand config, account settings
│
└── assets/
    ├── css/
    │   ├── custom.css               # Entry point
    │   ├── _brand.css               # SJ Interiors brand tokens (purple/gold)
    │   ├── _typography.css          # Font stacks
    │   ├── _layout.css              # Sidebar, mobile nav, grid
    │   ├── _surfaces.css            # Cards, surfaces
    │   └── _interactions.css        # Buttons, forms, filters
    ├── js/
    │   └── admin.js                 # Client-side behaviors
    ├── icon-192.png                 # PWA icon
    └── icon-512.png                 # PWA icon
```

---

## 2. New Database Tables

### `admin_users` — Admin authentication
```sql
create table if not exists admin_users (
    id uuid primary key default gen_random_uuid(),
    username text unique not null,
    password_hash text not null,
    full_name text,
    is_active boolean default true,
    created_at timestamptz default now()
);
```

### `documents` — Proposals, quotations, invoices
```sql
create type document_kind as enum ('proposal', 'quotation', 'invoice');
create type document_status as enum ('draft', 'sent', 'viewed', 'accepted', 'declined', 'paid', 'expired');

create table if not exists documents (
    id uuid primary key default gen_random_uuid(),
    kind document_kind not null,
    document_number text unique not null,
    inquiry_id uuid references inquiries(id),
    customer_name text not null,
    customer_phone text,
    customer_email text,
    title text not null,
    subtitle text,
    notes text,
    terms text,
    status document_status default 'draft',
    valid_until date,
    total_amount numeric(12,2) default 0,
    currency text default 'NGN',
    access_token text unique default gen_random_uuid()::text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
```

### `document_items` — Line items for documents
```sql
create table if not exists document_items (
    id uuid primary key default gen_random_uuid(),
    document_id uuid references documents(id) on delete cascade,
    description text not null,
    quantity numeric(10,2) default 1,
    unit_price numeric(12,2) not null,
    total numeric(12,2) generated always as (quantity * unit_price) stored,
    sort_order int default 0,
    created_at timestamptz default now()
);
```

---

## 3. Pages — Detailed Specifications

### 3.1 Login Page (`/login`)
**Layout**: Centered card on dark gradient background with SJ Interiors logo
- Username + password fields
- "Sign In" button with loading state
- Session-based auth (8-hour rolling TTL)
- Redirects to `/` after login

### 3.2 Dashboard Overview (`/`)
**Layout**: Metrics row + quick actions + recent activity

**Metrics Row** (4 cards):
- **Total Products** — count with icon
- **Active Inquiries** — count of `status='new'` inquiries
- **Orders Processing** — count of `status='processing'` orders
- **Revenue This Month** — sum of order totals

**Quick Actions Grid**:
- "Add Product" → `/products?new=1`
- "New Proposal" → `/documents?kind=proposal&new=1`
- "View Inquiries" → `/inquiries`
- "Settings" → `/settings`

**Recent Activity Feed**:
- Last 5 inquiries (with status badges)
- Last 5 orders (with status badges)
- Auto-refreshes every 30s via HTMX `AutoRefresh`

### 3.3 Categories Management (`/categories`)
**Layout**: Two-panel workspace (list + editor)

**List Panel**:
- Searchable list of all categories
- Each row: icon, label, slug, sort_order, active toggle
- "Add Category" button

**Editor Panel** (on select or Add):
- Label (text)
- Slug (text, auto-generated from label)
- Description (textarea)
- Icon (Bootstrap icon picker or text input)
- Image URL (with media library picker)
- Sort Order (number)
- Is Active (toggle)
- Save/Delete buttons

### 3.4 Products Management (`/products`)
**Layout**: Two-panel workspace (list + editor)

**List Panel**:
- Search + category filter pills
- Each row: thumbnail, name, category, price, stock status, featured toggle
- "Add Product" button

**Editor Panel**:
- Name (text)
- Slug (text, auto-generated)
- Category (select from categories)
- Price (text, e.g. "NGN 24,500")
- Description (textarea)
- Highlight/Badge text (text)
- Stock Status (select: In Stock / Made to Order / Discontinued)
- Is Featured (toggle)
- Is Active (toggle)
- Primary Image URL (with media library picker)
- Gallery Images (JSONB array, media picker)
- Save/Delete buttons

### 3.5 Services Management (`/services`)
**Layout**: Two-panel workspace (list + editor)

**List Panel**:
- Each row: icon, title, sort_order, active toggle
- "Add Service" button

**Editor Panel**:
- Title (text)
- Slug (text, auto-generated)
- Summary (textarea, short)
- Description (textarea, full)
- Icon (Bootstrap icon)
- Image URL (media picker)
- Sort Order (number)
- Is Active (toggle)
- Save/Delete buttons

### 3.6 Inquiry Inbox (`/inquiries`)
**Layout**: Two-panel workspace (list + detail)

**List Panel**:
- Filter pills: All / New / Contacted / Ordered / Closed
- Each row: customer name, source badge, status, date
- Unread indicator for `status='new'`

**Detail Panel**:
- Customer info: name, phone, email
- Source badge
- Message content
- Selected services (if service inquiry)
- Linked product (if product inquiry)
- Status dropdown (New → Contacted → Ordered → Closed)
- Internal notes textarea
- Quick action: "Convert to Order" button
- Quick action: "Create Proposal" button
- Quick action: "WhatsApp" button

### 3.7 Orders Pipeline (`/orders`)
**Layout**: Two-panel workspace (list + detail)

**List Panel**:
- Filter pills: All / Processing / Shipped / Delivered / Cancelled
- Each row: order number, customer, items count, status badge, date

**Detail Panel**:
- Order number (generated: SJ-YYYY-NNNN)
- Customer info
- Items list (JSONB, editable)
- Status dropdown with timeline visualization
- Notes textarea
- Created/updated timestamps

### 3.8 Document Workspace (`/documents`)
**Layout**: Two-panel workspace (list + editor)

**List Panel**:
- Filter pills: All / Proposals / Quotations / Invoices
- Filter by status: Draft / Sent / Viewed / Accepted / Declined / Paid
- Each row: document number, kind badge, customer, total, status, date
- "New Document" dropdown: Proposal / Quotation / Invoice

**Editor Panel**:
- **Header Section**: Document kind, number, title, subtitle
- **Customer Section**: Name, phone, email, link to inquiry
- **Line Items Table**: Dynamic rows with auto-calculate totals
- **Notes & Terms**: Internal notes, terms & conditions
- **Actions**: Save as Draft, Generate PDF, Send to Customer, Copy link

### 3.9 Media Library (`/media`)
**Layout**: Grid gallery with upload
- Grid of all uploaded images
- Upload button (drag & drop or file picker)
- Click to view/edit metadata
- Delete with confirmation
- Uploads to Supabase Storage `admin-media` bucket

### 3.10 Settings (`/settings`)
**Layout**: Stacked cards
- **Brand Configuration**: Business name, subtitle, tagline, WhatsApp, phones, address, socials
- **Hero Slides**: List with add/remove/reorder
- **Value Points**: List with add/remove
- **Wholesale Benefits**: List with add/remove
- **Account**: Change username/password

---

## 4. Document Generation

### 4.1 PDF Generation
- Use **ReportLab** for PDF generation
- Branded PDF templates with SJ Interiors purple/gold colors

### 4.2 Public Document Portal
- Each document gets a unique `access_token`
- Public URL: `/documents/{token}` (no auth required)
- Shows document with accept/decline buttons

### 4.3 Document Numbering
- Proposals: `PRO-YYYY-NNNN`
- Quotations: `QTN-YYYY-NNNN`
- Invoices: `INV-YYYY-NNNN`
- Auto-incrementing per year

---

## 5. Navigation Structure

### Desktop Sidebar
- **Brand Block**: SJ Interiors logo initials + "Admin" subtitle
- **Overview**: Dashboard (standalone)
- **Content Group**: Categories, Products, Services
- **Business Group**: Inquiries, Orders, Documents
- **Tools Group**: Media, Settings

### Mobile Bottom Nav (4 items + Menu)
- Overview, Products, Inquiries, Documents, Menu (drawer)

---

## 6. Theme & Branding

### Color Palette (matching public site)
- Primary: `#6E45C9` (purple)
- Secondary: `#D8BC73` (gold)
- Success: `#6CD8A4`
- Danger: `#FF727E`
- Dark BG: `#1a1128`
- Surface: `rgba(110, 69, 201, 0.08)`

### Typography
- Headings: Space Grotesk (400-700)
- Body: Inter (300-600)

### Design Language
- Dark-first glassmorphism (backdrop-filter: blur)
- Rounded cards with subtle shadows
- Purple accent on active states
- Gold for secondary actions

---

## 7. Implementation Phases

### Phase A — Foundation (Days 1-2)
1. Create project structure
2. Set up `config.py`, `theme.py`, `main.py`
3. Implement auth (login/logout/session)
4. Build `shell.py` (sidebar, bottom nav, mobile drawer)
5. Create login page
6. Set up CSS architecture

### Phase B — Dashboard (Day 3)
1. Dashboard overview with metrics
2. Quick actions grid
3. Recent activity feed
4. Auto-refresh polling

### Phase C — Content Management (Days 4-6)
1. Categories CRUD
2. Products CRUD
3. Services CRUD
4. Media library with Supabase Storage

### Phase D — Business Tools (Days 7-9)
1. Inquiry inbox with status management
2. Orders pipeline
3. Document workspace (proposals/quotations/invoices)
4. PDF generation with ReportLab
5. Public document portal

### Phase E — Settings & Polish (Days 10-11)
1. Brand config management
2. Hero slides management
3. Account settings
4. PWA setup
5. Testing

### Phase F — Deployment (Day 12)
1. Vercel configuration
2. Environment variables
3. Schema deployment
4. Seed data
5. Final testing

---

## 8. Key Files to Reference

- `C:\Users\Meshell\Desktop\FastHTML\neo-admin\app\main.py` — App shell pattern
- `C:\Users\Meshell\Desktop\FastHTML\neo-admin\app\presentation\shell.py` — Layout pattern
- `C:\Users\Meshell\Desktop\FastHTML\neo-admin\app\schema.py` — Declarative CRUD
- `C:\Users\Meshell\Desktop\FastHTML\neo-admin\app\infrastructure\deal_pdf.py` — PDF generation
- `C:\Users\Meshell\Desktop\FastHTML\neo-admin\app\presentation\pages\deals.py` — Document workspace
- `C:\Users\Meshell\Desktop\FastHTML\sj_interiors\supabase_schema.sql` — Current schema
- `C:\Users\Meshell\Desktop\FastHTML\sj_interiors\components.py` — Brand styling reference
