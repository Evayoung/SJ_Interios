-- Supabase schema for SJ Interiors

create extension if not exists "pgcrypto";

create type order_status as enum ('processing', 'shipped', 'delivered', 'cancelled');
create type inquiry_status as enum ('new', 'contacted', 'ordered', 'closed');
create type stock_status as enum ('in_stock', 'made_to_order', 'discontinued');
create type inquiry_source as enum ('whatsapp', 'contact_form', 'phone', 'services_page');

create table if not exists categories (
    id uuid primary key default gen_random_uuid(),
    slug text unique not null,
    label text not null,
    description text,
    icon text,
    image_url text,
    sort_order int default 0,
    is_active boolean default true,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists products (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    slug text unique not null,
    category_slug text,
    description text,
    price text,
    highlight text,
    image_url text,
    images jsonb,
    stock_status stock_status default 'in_stock',
    is_featured boolean default false,
    is_active boolean default true,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists services (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    slug text unique not null,
    summary text,
    description text,
    icon text,
    image_url text,
    is_active boolean default true,
    sort_order int default 0,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists inquiries (
    id uuid primary key default gen_random_uuid(),
    product_id uuid,
    service_inquiry boolean default false,
    customer_name text,
    phone text,
    email text,
    message text,
    source inquiry_source default 'contact_form',
    selected_services jsonb,
    status inquiry_status default 'new',
    created_at timestamptz default now()
);

create table if not exists orders (
    id uuid primary key default gen_random_uuid(),
    inquiry_id uuid,
    order_number text unique not null,
    customer_name text,
    phone text,
    items jsonb,
    status order_status default 'processing',
    notes text,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

create table if not exists brand_config (
    id uuid primary key default gen_random_uuid(),
    key text unique not null,
    value jsonb,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
