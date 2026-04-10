"""Reusable page components for the SJ Interiors website."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from fasthtml.common import *

from faststrap import Badge, Button, Card, Carousel, CarouselItem, Col, Container, Icon, Navbar, Row

try:
    from .content import (
        ADDRESS,
        BUSINESS_NAME,
        BUSINESS_SUBTITLE,
        CATEGORIES,
        HERO_SLIDES,
        PHONE_NUMBER,
        PHONE_NUMBERS,
        SHORT_INTRO,
        SOCIALS,
        TAGLINE,
        VALUE_POINTS,
        WHATSAPP_NUMBER,
        WHOLESALE_BENEFITS,
        category_label,
    )
except ImportError:
    from content import (
        ADDRESS,
        BUSINESS_NAME,
        BUSINESS_SUBTITLE,
        CATEGORIES,
        HERO_SLIDES,
        PHONE_NUMBER,
        PHONE_NUMBERS,
        SHORT_INTRO,
        SOCIALS,
        TAGLINE,
        VALUE_POINTS,
        WHATSAPP_NUMBER,
        WHOLESALE_BENEFITS,
        category_label,
    )


def whatsapp_url(message: str) -> str:
    """Build a WhatsApp deep link for storefront actions."""
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def section_intro(eyebrow: str, title: str, copy: str, align: str = "start") -> Div:
    """Shared intro block for major sections."""
    text_cls = "text-center" if align == "center" else "text-start"
    margin_cls = "mx-auto" if align == "center" else ""
    return Div(
        Badge(eyebrow, variant="light", cls="section-eyebrow"),
        H2(title, cls=f"section-title {text_cls}"),
        P(copy, cls=f"section-copy {text_cls} {margin_cls}"),
        cls="section-heading",
    )


def nav_link(label: str, href: str, current_path: str) -> A:
    """Create a styled navigation link with active state."""
    active = "nav-current" if current_path == href else ""
    return A(label, href=href, cls=f"nav-link {active}")


def site_nav(current_path: str) -> Nav:
    """Top navigation shared across pages."""
    brand = Div(
        Span("SJ Interiors", cls="brand-name"),
        Span(BUSINESS_SUBTITLE, cls="brand-subtitle"),
        cls="brand-lockup d-flex flex-column",
    )
    nav_items = Div(
        nav_link("Home", "/", current_path),
        nav_link("Shop", "/shop", current_path),
        nav_link("About", "/about", current_path),
        nav_link("Contact", "/contact", current_path),
        cls="navbar-nav ms-lg-auto me-lg-3 align-items-lg-center gap-2",
    )
    nav_cta = Div(
        Button("Shop Now", href="/shop", cls="site-nav-cta px-4"),
        cls="d-flex align-items-center mt-3 mt-lg-0",
    )
    return Navbar(
        nav_items,
        nav_cta,
        brand=brand,
        brand_href="/",
        fixed="top",
        id="site-nav",
        cls="site-nav shadow-sm px-2",
    )


def footer_social_links() -> Div:
    """Social icon set used in the footer."""
    return Div(
        *[
            A(
                Icon(item["icon"]),
                href=item["href"],
                target="_blank",
                rel="noreferrer",
                aria_label=item["label"],
                cls="social-icon",
            )
            for item in SOCIALS
        ],
        cls="d-flex gap-2 justify-content-start",
    )


def site_footer() -> Div:
    """Shared footer with contacts and social links."""
    return Div(
        Container(
            Row(
                Col(
                    H3("SJ Interiors", cls="footer-brand"),
                    P(
                        "Redefining your space with curtains, blinds, bedding, pillows, and finishing touches designed for stylish living.",
                        cls="footer-copy",
                    ),
                    footer_social_links(),
                    lg=5,
                    cols=12,
                    cls="mb-4 mb-lg-0",
                ),
                Col(
                    H4("Quick Links", cls="footer-title"),
                    A("Home", href="/", cls="footer-link d-block"),
                    A("Shop", href="/shop", cls="footer-link d-block"),
                    A("About", href="/about", cls="footer-link d-block"),
                    A("Contact", href="/contact", cls="footer-link d-block"),
                    lg=3,
                    md=6,
                    cols=12,
                    cls="mb-4 mb-md-0",
                ),
                Col(
                    H4("Reach Us", cls="footer-title"),
                    *[P(number, cls="footer-link") for number in PHONE_NUMBERS],
                    P("@sj_interior_deco_and_beddings", cls="footer-link"),
                    P(ADDRESS, cls="footer-link"),
                    P("Retail and wholesale orders available", cls="footer-link"),
                    lg=4,
                    md=6,
                    cols=12,
                ),
                cls="g-4", cols=1, cols_md=2, cols_lg=3
            ),
            Div(
                P(
                    "Simplicity. Comfort. Style.",
                    cls="footer-note mb-0",
                ),
                cls="footer-base mt-4 pt-4",
            ),
        ),
        cls="site-footer mt-5",
    )


def floating_whatsapp_button() -> A:
    """Floating WhatsApp entry point."""
    return A(
        Icon("whatsapp"),
        Span("WhatsApp Us", cls="ms-2"),
        href=whatsapp_url("Hello SJ Interiors, I would like to place an order."),
        target="_blank",
        rel="noreferrer",
        aria_label="Chat with SJ Interiors on WhatsApp",
        cls="floating-whatsapp",
    )


def hero_section() -> Div:
    """Home page hero with auto-scrolling carousel background."""
    slides = [
        CarouselItem(
            Img(
                src=slide.image,
                alt=slide.alt,
                cls="d-block w-100 hero-slide-image",
                loading="eager" if index == 0 else "lazy",
            ),
            active=index == 0,
        )
        for index, slide in enumerate(HERO_SLIDES)
    ]
    highlight_card = Card(
        Badge("Wholesale + Retail", cls="hero-side-badge mb-3"),
        H3("Style homes, short-let spaces, and guest rooms with ease.", cls="hero-side-title"),
        P(
            "From bedsheets and duvets to curtains, blinds, pillows, and decor accessories, "
            "SJ Interiors helps you create a soft, cohesive finish.",
            cls="hero-side-copy",
        ),
        Div(
            Div(Span("06"), Small("key services"), cls="hero-stat"),
            Div(Span("Retail"), Small("& wholesale"), cls="hero-stat"),
            cls="d-flex flex-wrap gap-3 mt-4",
        ),
        cls="hero-side-card border-0",
        body_cls="p-4 p-lg-5 d-none d-lg-block",
    )
    return Div(
        Div(
            Carousel(
                *slides,
                carousel_id="sjHero",
                controls=True,
                indicators=True,
                interval=4200,
                ride="carousel",
                pause=False,
                wrap=True,
                fade=True,
                cls="hero-carousel",
            ),
            cls="hero-carousel-layer",
        ),
        Div(Div(cls="hero-overlay"), cls="hero-overlay-layer"),
        Div(
            Container(
                Row(
                    Col(
                        Div(
                            Badge("Modern home essentials", variant="light", cls="hero-badge"),
                            H1(BUSINESS_NAME, cls="hero-title"),
                            P(TAGLINE, cls="hero-copy"),
                            Div(
                                Button(
                                    "Shop the Collection", 
                                    href="/shop", 
                                    cls="px-3 py-2",
                                    style="max-width: 80%;"
                                    ),
                                Button(
                                    "Order on WhatsApp",
                                    href=whatsapp_url(
                                        "Hello SJ Interiors, I want to shop for bedding and interior decor."
                                    ),
                                    target="_blank",
                                    rel="noreferrer",
                                    variant="light",
                                    cls="hero-outline-btn px-3 py-2",
                                    style="max-width: 80%;"
                                ),
                                cls="d-flex flex-column flex-md-row gap-3 mt-4 w-100 justify-content-center justify-content-lg-start",
                            ),
                            Div(
                                Span("Bedsheets"),
                                Span("Duvets"),
                                Span("Curtains"),
                                Span("Blinds"),
                                Span("Pillows"),
                                cls="hero-chip-row mt-4",
                            ),
                            cls="hero-copy-wrap justify-content-center justify-content-lg-start w-100 px-3",
                        ),
                        lg=7,
                        cols=12,
                    ),
                    Col(highlight_card, lg=5, cols=12, cls="mt-4 mt-lg-0"),
                    cls="align-items-center hero-content-row", cols=1, cols_lg=2
                ),
                cls="hero-content position-relative",
            ),
            cls="hero-content-layer",
        ),
        cls="hero-shell position-relative overflow-hidden",
    )


def category_card(category: Any) -> Card:
    """Featured category card used on the home page."""
    return Card(
        Badge(category.label, variant="light", cls="category-badge"),
        H3(category.label, cls="category-title"),
        P(category.description, cls="category-copy"),
        Div(Icon(category.icon), cls="category-icon"),
        img_top=category.image,
        cls="category-card border-0 h-100",
        body_cls="position-relative p-4",
    )


def featured_categories_section() -> Div:
    """Home page category highlights."""
    featured = CATEGORIES[:5]
    return Div(
        Container(
            section_intro(
                "Featured categories",
                "Everything you need to make a space feel soft, polished, and premium.",
                "Explore our most-requested collections for bedrooms, windows, and everyday styling.",
            ),
            Row(
                *[
                    Col(category_card(category), lg=4, cols=12, cls="mb-4")
                    for category in featured
                ],
                cls="g-4 mt-1", cols=1, cols_md=2, cols_lg=3
            ),
        ),
        cls="content-section",
    )


def product_card(product: Any) -> Card:
    """Product card for the shop grid."""
    message = (
        f"Hello SJ Interiors, I want to order the {product.name} "
        f"({category_label(product.category)}) priced at {product.price}."
    )
    return Card(
        Badge(product.highlight, variant="light", cls="product-badge"),
        H3(product.name, cls="product-title"),
        P(category_label(product.category), cls="product-category"),
        P(product.description, cls="product-copy"),
        Div(
            Span(product.price, cls="product-price"),
            Button(
                "Order on WhatsApp",
                href=whatsapp_url(message),
                target="_blank",
                rel="noreferrer",
                size="sm",
                cls="product-btn",
            ),
            cls="d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-3 mt-auto",
        ),
        img_top=product.image,
        cls="product-card border-0 h-100",
        body_cls="p-4 d-flex flex-column gap-2",
    )


def product_grid(products: list[Any]) -> Div:
    """Responsive product grid."""
    return Div(
        Row(
            *[Col(product_card(product), lg=4, cols=12, cls="mb-4") for product in products],
            cls="g-4", cols=1, cols_md=2, cols_lg=3
        ),
        cls="product-grid",
    )


def shop_filter_bar(active_category: str) -> Div:
    """Link-based category filter pills."""
    filter_items = [("all", "All")]
    filter_items.extend((category.slug, category.label) for category in CATEGORIES)
    return Div(
        *[
            A(
                label,
                href="/shop" if slug == "all" else f"/shop?category={slug}",
                cls=f"filter-pill {'is-active' if active_category == slug else ''}",
            )
            for slug, label in filter_items
        ],
        cls="filter-bar d-flex flex-wrap gap-2",
    )


def home_preview_section(products: list[Any]) -> Div:
    """Curated preview of products on the home page."""
    preview_products = products[:6]
    return Div(
        Container(
            section_intro(
                "Shop preview",
                "Rounded, refined product displays built for easy WhatsApp ordering.",
                "Customers can browse styles quickly, then jump straight into a WhatsApp conversation to order.",
                align="start",
            ),
            product_grid(preview_products),
            Div(
                Button("Browse Full Shop", href="/shop", cls="px-4"),
                cls="text-center mt-3",
            ),
        ),
        cls="content-section content-section-soft",
    )


def lookbook_section() -> Div:
    """Editorial lookbook block for the home page."""
    return Div(
        Container(
            Row(
                Col(
                    section_intro(
                        "Why SJ Interiors?",
                        "A warm brand experience that still feels premium and professional.",
                        SHORT_INTRO,
                        align="start",
                    ),
                    Div(
                        *[
                            Card(
                                H3(title, cls="value-title"),
                                P(copy, cls="value-copy"),
                                cls="value-card border-0 mb-3",
                                body_cls="p-4",
                            )
                            for title, copy in VALUE_POINTS
                        ],
                        cls="mt-4",
                    ),
                    lg=5,
                    cols=12,
                ),
                Col(
                    Div(
                        Img(
                            src="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1400&q=80",
                            alt="Styled sitting room with curtains and decor accents",
                            cls="lookbook-image lookbook-main",
                            loading="lazy",
                        ),
                        Img(
                            src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=900&q=80",
                            alt="Decorative throw pillows on a modern sofa",
                            cls="lookbook-image lookbook-float",
                            loading="lazy",
                        ),
                        Div(
                            Badge("Decor edit", variant="warning", cls="lookbook-badge"),
                            P(
                                "Mix bedding, pillows, windows, and soft gold accents for a finished look.",
                                cls="lookbook-note mb-0",
                            ),
                            cls="lookbook-note-card",
                        ),
                        cls="lookbook-stack",
                    ),
                    # lg=7,
                    cols=12,
                    cls="mt-4 mt-lg-0",
                ),
                cls="align-items-center g-4", cols=1, cols_md=2
            )
        ),
        cls="content-section",
    )


def wholesale_cta_section() -> Div:
    """Wholesale and retail CTA strip."""
    return Div(
        Container(
            Row(
                Col(
                    Badge("Wholesale & retail", variant="light", cls="section-eyebrow mb-2"),
                    H2(
                        "Need a room refresh or a larger project supply order?",
                        cls="cta-title",
                    ),
                    P(
                        "We support one-off purchases and larger orders for hospitality spaces, resellers, and interior styling projects.",
                        cls="cta-copy",
                    ),
                    Div(
                        Button(
                            "Start on WhatsApp",
                            href=whatsapp_url(
                                "Hello SJ Interiors, I need a quote for curtains, bedding, blinds, or a wholesale order."
                            ),
                            target="_blank",
                            rel="noreferrer",
                            cls="px-4",
                        ),
                        Button("Read Our Story", href="/about", variant="light", cls="cta-light-btn"),
                        cls="d-flex flex-column flex-sm-row gap-3 mt-4",
                    ),
                    lg=6,
                    cols=12,
                    cls="order-md-2 order-1",
                ),
                Col(
                    Div(
                        *[
                            Div(Icon("check2-circle", cls="me-2"), Span(item), cls="cta-list-item")
                            for item in WHOLESALE_BENEFITS
                        ],
                        cls="cta-list",
                    ),
                    lg=6,
                    cols=12,
                    cls="mt-4 mt-lg-0",
                ),
                cls="align-items-center g-4", cols=1, cols_md=2,
            )
        ),
        cls="content-section content-section-cta",
    )


def page_intro_banner(eyebrow: str, title: str, copy: str) -> Div:
    """Header band for interior pages."""
    return Div(
        Container(
            Badge(eyebrow, variant="light", cls="section-eyebrow mb-2"),
            H1(title, cls="interior-title"),
            P(copy, cls="interior-copy"),
        ),
        cls="interior-hero",
    )


def page_shell(page_title: str, current_path: str, *sections: Any) -> tuple[Any, ...]:
    """Compose a complete page with shared shell pieces."""
    return (
        Title(f"{page_title} | {BUSINESS_NAME}"),
        Div(
            site_nav(current_path),
            Main(*sections, cls="site-main"),
            site_footer(),
            floating_whatsapp_button(),
            cls="site-app",
        ),
    )
