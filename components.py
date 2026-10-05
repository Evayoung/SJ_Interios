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
        SERVICE_CATEGORIES,
        SHORT_INTRO,
        SOCIALS,
        TAGLINE,
        TESTIMONIALS,
        TRANSFORMATIONS,
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
        SERVICE_CATEGORIES,
        SHORT_INTRO,
        SOCIALS,
        TAGLINE,
        TESTIMONIALS,
        TRANSFORMATIONS,
        VALUE_POINTS,
        WHATSAPP_NUMBER,
        WHOLESALE_BENEFITS,
        category_label,
    )


def whatsapp_url(message: str, phone: str = "") -> str:
    """Build a WhatsApp deep link for storefront actions."""
    if not phone:
        try:
            from services import get_whatsapp_number
            phone = get_whatsapp_number()
        except Exception:
            phone = WHATSAPP_NUMBER
    clean_phone = str(phone).replace("+", "").replace(" ", "").replace("-", "")
    return f"https://wa.me/{clean_phone}?text={quote(message)}"


def _value(item: Any, key: str, fallback: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, fallback)
    return getattr(item, key, fallback)


def _product_value(product: Any, key: str, fallback: Any = None) -> Any:
    if isinstance(product, dict):
        return product.get(key, fallback)
    return getattr(product, key, fallback)


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
        nav_link("Services", "/services", current_path),
        nav_link("About", "/about", current_path),
        nav_link("Contact", "/contact", current_path),
        cls="navbar-nav ms-lg-auto me-lg-3 align-items-lg-center gap-2",
    )
    nav_cta = Div(
        Button("Shop Now", href="/shop", cls="site-nav-cta px-4"),
        cls="d-flex align-items-center mt-3 mt-lg-0",
    )
    theme_toggle = Button(
        Icon("moon"),
        cls="theme-toggle ms-2",
        onclick="toggleTheme()",
        aria_label="Toggle dark mode",
    )
    return Navbar(
        nav_items,
        nav_cta,
        theme_toggle,
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
                    A("Services", href="/services", cls="footer-link d-block"),
                    A("About", href="/about", cls="footer-link d-block"),
                    A("Contact", href="/contact", cls="footer-link d-block"),
                    A("Order Lookup", href="/order-lookup", cls="footer-link d-block"),
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


def hero_section(brand: dict[str, Any] | None = None, hero_slides: list[Any] | None = None) -> Div:
    """Home page hero with auto-scrolling carousel background."""
    brand = brand or {}
    hero_slides = hero_slides if hero_slides is not None else [
        {"image": slide.image, "alt": slide.alt} for slide in HERO_SLIDES
    ]
    business_name = brand.get("business_name", BUSINESS_NAME)
    tagline = brand.get("tagline", TAGLINE)
    slides = [
        CarouselItem(
            Img(
                src=slide.get("image"),
                alt=slide.get("alt", ""),
                cls="d-block w-100 hero-slide-image",
                loading="eager" if index == 0 else "lazy",
            ),
            active=index == 0,
        )
        for index, slide in enumerate(hero_slides)
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


def featured_categories_section(categories: list[Any] | None = None) -> Div:
    """Home page category highlights."""
    categories = categories if categories is not None else CATEGORIES
    featured = categories[:5]
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
    """Product card for the shop grid with Quick View, high-contrast buttons, and mobile-friendly stacking."""
    name = _product_value(product, "name", "Product")
    slug = _product_value(product, "slug", name.lower().replace(" ", "-").replace("&", "and"))
    price = _product_value(product, "price", "")
    highlight = _product_value(product, "highlight", "")
    description = _product_value(product, "description", "")
    image = _product_value(product, "image_url", _product_value(product, "image", ""))
    category_slug = _product_value(product, "category_slug", _product_value(product, "category", ""))
    message = (
        f"Hello SJ Interiors, I want to order the {name} "
        f"({category_label(category_slug)}) priced at {price}."
    )

    clean_price_val = price.replace("NGN", "").replace(",", "").strip()

    return Card(
        Div(
            Badge(highlight, variant="light", cls="product-badge text-dark border") if highlight else None,
            Button(
                Icon("eye", cls="me-1"), "Quick View",
                type="button",
                cls="btn btn-sm btn-white border text-dark product-quickview-btn shadow-sm",
                hx_get=f"/shop/product-modal/{slug}",
                hx_target="#quickViewModalBody",
                hx_swap="innerHTML",
                data_bs_toggle="modal",
                data_bs_target="#quickViewModal",
            ),
            cls="d-flex justify-content-between align-items-start position-relative w-100",
        ),
        H3(name, cls="product-title fs-5 fw-bold text-dark mb-1"),
        P(category_label(category_slug), cls="product-category small text-muted mb-2"),
        P(description, cls="product-copy small text-secondary line-clamp-2 mb-3"),
        Div(
            Div(Span(price, cls="product-price fs-5 fw-bold text-dark"), cls="mb-2 mb-sm-0"),
            Div(
                Button(
                    Icon("bag-plus", cls="me-1"), "Add",
                    type="button",
                    cls="btn btn-outline-dark btn-sm flex-fill d-flex align-items-center justify-content-center",
                    title="Add to WhatsApp Quote Bag",
                    onclick=f"""
                        window.addToQuoteBag({{
                            id: '{slug}',
                            name: '{name.replace("'", "")}',
                            price: '{price}',
                            priceNum: {clean_price_val or 0},
                            image: '{image}',
                            category: '{category_slug}'
                        }});
                    """,
                ),
                A(
                    Icon("whatsapp", cls="me-1"), "Order",
                    href=whatsapp_url(message),
                    target="_blank",
                    rel="noreferrer",
                    cls="btn btn-success btn-sm flex-fill d-flex align-items-center justify-content-center fw-semibold text-white",
                    title="Direct WhatsApp Order",
                ),
                cls="d-flex gap-2 w-100 w-sm-auto",
            ),
            cls="d-flex flex-column flex-sm-row align-items-sm-center justify-content-between gap-2 mt-auto pt-3 border-top",
        ),
        img_top=image,
        cls="product-card border-0 shadow-sm h-100 bg-white",
        body_cls="p-3 p-md-4 d-flex flex-column",
    )


def product_grid(products: list[Any]) -> Div:
    """Responsive product grid."""
    if not products:
        return Div(
            Card(
                Div(
                    Icon("search", size="2.5rem", cls="text-muted mb-3"),
                    H4("No products found", cls="mb-2"),
                    P("Try adjusting your search terms or category filter.", cls="text-muted"),
                    A("View All Products", href="/shop", cls="btn btn-primary btn-sm mt-2"),
                    cls="p-5 text-center",
                ),
                cls="border-0 shadow-sm",
            ),
            cls="my-4",
        )

    return Div(
        Row(
            *[Col(product_card(product), lg=4, cols=12, cls="mb-4") for product in products],
            cls="g-4", cols=1, cols_md=2, cols_lg=3
        ),
        cls="product-grid",
    )


def shop_search_and_sort_bar(active_category: str = "all", active_sort: str = "featured", query: str = "", categories: list[Any] | None = None) -> Div:
    """Integrated Category Tabs, Live Search debounced bar, and Sort selector."""
    categories = categories if categories is not None else CATEGORIES
    filter_items = [("all", "All")]
    filter_items.extend(( _value(category, "slug"), _value(category, "label") ) for category in categories)

    category_pills = Div(
        *[
            A(
                label,
                href=f"/shop?category={slug}&sort={active_sort}&q={query}" if slug != "all" else f"/shop?sort={active_sort}&q={query}",
                cls=f"filter-pill {'is-active' if active_category == slug else ''}",
            )
            for slug, label in filter_items
        ],
        cls="filter-bar d-flex flex-wrap gap-2 mb-3",
    )

    search_and_sort = Form(
        Row(
            Col(
                Div(
                    Span(Icon("search"), cls="input-group-text bg-white border-end-0 text-muted"),
                    Input(
                        type="search",
                        name="q",
                        value=query,
                        placeholder="Search bedsheets, blackout curtains, velvet pillows, blinds...",
                        cls="form-control border-start-0 ps-0",
                        hx_get="/shop/results",
                        hx_trigger="keyup changed delay:350ms, search",
                        hx_target="#product-results-container",
                        hx_include="closest form",
                    ),
                    cls="input-group",
                ),
                lg=7, cols=12, cls="mb-2 mb-lg-0",
            ),
            Col(
                Div(
                    Input(type="hidden", name="category", value=active_category),
                    Select(
                        Option("Featured Collection", value="featured", selected=active_sort == "featured"),
                        Option("Price: Low to High", value="price_asc", selected=active_sort == "price_asc"),
                        Option("Price: High to Low", value="price_desc", selected=active_sort == "price_desc"),
                        Option("Name: A to Z", value="name_asc", selected=active_sort == "name_asc"),
                        name="sort",
                        cls="form-select",
                        hx_get="/shop/results",
                        hx_target="#product-results-container",
                        hx_include="closest form",
                    ),
                    cls="d-flex align-items-center gap-2",
                ),
                lg=5, cols=12,
            ),
            cls="g-2 align-items-center",
        ),
        method="get",
        action="/shop",
        cls="shop-controls-form mb-4 p-3 bg-light rounded-3 border",
    )

    return Div(category_pills, search_and_sort)


def shop_filter_bar(active_category: str, categories: list[Any] | None = None) -> Div:
    """Link-based category filter pills."""
    return shop_search_and_sort_bar(active_category=active_category, categories=categories)


def home_preview_section(products: list[Any]) -> Div:
    """Curated preview of products on the home page."""
    preview_products = products[:6]
    return Div(
        Container(
            section_intro(
                "Featured Collections",
                "Crafted for comfort, styled for everyday elegance.",
                "Explore our curated selection of bespoke curtains, luxury bedding, and statement interior essentials.",
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


def wholesale_cta_section(brand: dict[str, Any] | None = None) -> Div:
    """Wholesale and retail CTA strip."""
    brand = brand or {}
    wholesale_benefits = brand.get("wholesale_benefits", WHOLESALE_BENEFITS)
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


def testimonials_section(testimonials: list[dict] | None = None) -> Div:
    """Customer testimonials and trust showcase."""
    testimonials = testimonials or TESTIMONIALS
    cards = []
    for t in testimonials:
        cards.append(
            Col(
                Card(
                    Div(
                        *[Icon("star-fill", cls="text-warning me-1") for _ in range(t.get("rating", 5))],
                        cls="d-flex mb-2",
                    ),
                    P(f'"{t.get("review", "")}"', cls="fst-italic text-secondary mb-3 flex-grow-1"),
                    Div(
                        Div(
                            P(t.get("name", ""), cls="fw-bold mb-0 text-dark"),
                            Small(f'{t.get("role", "")} · {t.get("location", "")}', cls="text-muted"),
                        ),
                        Badge(t.get("item", "Custom Decor"), variant="light", cls="ms-auto small"),
                        cls="d-flex align-items-center justify-content-between pt-3 border-top mt-auto",
                    ),
                    cls="h-100 border-0 shadow-sm p-3",
                    body_cls="d-flex flex-column h-100 p-2",
                ),
                lg=4, cols=12, cls="mb-3",
            )
        )
    return Div(
        Container(
            section_intro(
                "Client Love & Reviews",
                "Trusted by Homeowners, Shortlet Hosts, & Decor Enthusiasts",
                "Here is what our clients in Ilorin and across Nigeria say about our fabrics, fittings, and swift delivery.",
                align="center",
            ),
            Row(*cards, cls="g-4 mt-2"),
        ),
        cls="content-section bg-light py-5",
    )


def before_after_section(transformations: list[dict] | None = None) -> Div:
    """Before & after room transformation showcase."""
    items = transformations or TRANSFORMATIONS
    cards = []
    for t in items:
        cards.append(
            Col(
                Card(
                    Img(src=t.get("image", ""), alt=t.get("title", ""), cls="card-img-top object-fit-cover", style="height: 18rem;"),
                    Div(
                        Badge(t.get("tag", "Makeover"), variant="warning", cls="mb-2"),
                        H3(t.get("title", ""), cls="h4 fw-bold mb-3"),
                        Div(
                            Div(
                                Span(Icon("x-circle", cls="text-danger me-2"), cls="fw-bold text-danger"),
                                Span(t.get("before_desc", ""), cls="small text-muted"),
                                cls="d-flex align-items-start mb-2",
                            ),
                            Div(
                                Span(Icon("check-circle-fill", cls="text-success me-2"), cls="fw-bold text-success"),
                                Span(t.get("after_desc", ""), cls="small text-dark fw-semibold"),
                                cls="d-flex align-items-start",
                            ),
                            cls="p-3 bg-light rounded-3",
                        ),
                        cls="p-4",
                    ),
                    cls="border-0 shadow-sm h-100 overflow-hidden",
                    body_cls="p-0",
                ),
                lg=6, cols=12, cls="mb-4",
            )
        )
    return Div(
        Container(
            section_intro(
                "Space Transformations",
                "From Bare Rooms to Styled Havens",
                "See the dramatic difference precision drapery, curated blinds, and hotel-soft bedding make in any living space.",
                align="center",
            ),
            Row(*cards, cls="g-4 mt-3"),
        ),
        cls="content-section py-5",
    )


def floating_quote_bag_button() -> Div:
    """Floating cart bag trigger with dynamic badge count."""
    return Div(
        Button(
            Icon("bag-check", size="1.4rem"),
            Span("0", id="cart-item-count", cls="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-warning text-dark border"),
            type="button",
            cls="btn btn-dark shadow-lg rounded-circle position-relative p-3",
            style="width: 3.5rem; height: 3.5rem; display: flex; align-items: center; justify-content: center;",
            data_bs_toggle="offcanvas",
            data_bs_target="#quoteBagOffcanvas",
            aria_controls="quoteBagOffcanvas",
            aria_label="Open WhatsApp Quote Bag",
            title="View Quote Bag",
        ),
        cls="floating-quote-bag-wrap position-fixed",
        style="bottom: 5.5rem; right: 1.5rem; z-index: 1040;",
    )


def quote_bag_drawer() -> Div:
    """Offcanvas / Drawer displaying items in the multi-item WhatsApp quote bag."""
    return Div(
        Div(
            Div(
                H5("Your WhatsApp Quote Bag", cls="offcanvas-title fw-bold mb-0"),
                Button(type="button", cls="btn-close text-reset", data_bs_dismiss="offcanvas", aria_label="Close"),
                cls="offcanvas-header border-bottom bg-light",
            ),
            Div(
                Div(
                    P("Your bag is currently empty.", cls="text-muted text-center py-5"),
                    id="quote-bag-items-list",
                    cls="quote-bag-body flex-grow-1 overflow-auto p-3",
                ),
                Div(
                    Div(
                        Span("Estimated Total:", cls="fw-bold"),
                        Span("NGN 0", id="quote-bag-subtotal", cls="fw-bold h5 mb-0 text-primary"),
                        cls="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom",
                    ),
                    Div(
                        Input(type="text", id="bag-customer-name", placeholder="Your Full Name (optional)", cls="form-control form-control-sm mb-2"),
                        Input(type="tel", id="bag-customer-phone", placeholder="Your Phone / Delivery City", cls="form-control form-control-sm mb-3"),
                        Button(
                            Icon("whatsapp", cls="me-2"), "Send Order to WhatsApp",
                            type="button",
                            cls="btn btn-success w-100 py-2 fw-bold shadow-sm",
                            onclick="window.dispatchQuoteBagToWhatsApp();",
                        ),
                        Button(
                            "Clear Bag",
                            type="button",
                            cls="btn btn-link btn-sm text-muted w-100 mt-1",
                            onclick="window.clearQuoteBag();",
                        ),
                        cls="quote-bag-checkout-box",
                    ),
                    cls="p-3 bg-light border-top mt-auto",
                ),
                cls="offcanvas-body d-flex flex-column p-0 h-100",
            ),
            cls="offcanvas-content h-100",
        ),
        cls="offcanvas offcanvas-end shadow-lg",
        tabindex="-1",
        id="quoteBagOffcanvas",
        aria_labelledby="quoteBagOffcanvasLabel",
        style="width: 24rem; max-width: 90vw;",
    )


def product_quick_view_modal() -> Div:
    """Bootstrap modal shell for product quick-view details."""
    return Div(
        Div(
            Div(
                Div(
                    Span("Product Overview", cls="modal-title h5 fw-bold"),
                    Button(type="button", cls="btn-close", data_bs_dismiss="modal", aria_label="Close"),
                    cls="modal-header border-bottom",
                ),
                Div(
                    Div("Loading product details...", cls="text-center py-5 text-muted"),
                    cls="modal-body p-4",
                    id="quickViewModalBody",
                ),
                cls="modal-content border-0 shadow",
            ),
            cls="modal-dialog modal-lg modal-dialog-centered",
        ),
        cls="modal fade",
        id="quickViewModal",
        tabindex="-1",
        aria_hidden="true",
    )


def quick_view_modal_fragment(product: Any) -> Div:
    """Render rich quick-view modal inner content."""
    if not product:
        return Div("Product not found.", cls="text-muted p-4 text-center")

    name = _product_value(product, "name", "Product")
    slug = _product_value(product, "slug", name.lower().replace(" ", "-"))
    price = _product_value(product, "price", "")
    description = _product_value(product, "description", "")
    image = _product_value(product, "image_url", _product_value(product, "image", ""))
    images = _product_value(product, "images", []) or []
    category_slug = _product_value(product, "category_slug", _product_value(product, "category", ""))
    highlight = _product_value(product, "highlight", "")
    stock_status = _product_value(product, "stock_status", "in_stock")

    clean_price_val = price.replace("NGN", "").replace(",", "").strip()
    direct_msg = f"Hello SJ Interiors, I want to order {name} ({price})."

    # Gallery thumbnails if extra images exist
    extra_thumbs = []
    if images and isinstance(images, list):
        for img_url in images[:4]:
            extra_thumbs.append(
                Img(src=img_url, cls="rounded border me-2", style="width: 4rem; height: 4rem; object-fit: cover; cursor: pointer;",
                    onclick=f"document.getElementById('quickViewMainImg').src = '{img_url}';")
            )

    return Row(
        Col(
            Div(
                Img(src=image, id="quickViewMainImg", alt=name, cls="w-100 rounded-3 object-fit-cover shadow-sm", style="max-height: 22rem;"),
                Div(*extra_thumbs, cls="d-flex mt-2 overflow-auto") if extra_thumbs else None,
                cls="mb-3 mb-md-0",
            ),
            md=6, cols=12,
        ),
        Col(
            Div(
                Div(
                    Badge(category_label(category_slug), variant="light", cls="me-2"),
                    Badge(highlight, variant="warning") if highlight else None,
                    Badge(stock_status.replace("_", " ").title(), variant="success" if stock_status == "in_stock" else "secondary", cls="ms-auto"),
                    cls="d-flex align-items-center mb-2",
                ),
                H2(name, cls="h3 fw-bold mb-2"),
                P(price, cls="h4 text-primary fw-bold mb-3"),
                P(description, cls="text-secondary mb-4"),
                Div(
                    Button(
                        Icon("bag-plus", cls="me-2"), "Add to WhatsApp Bag",
                        type="button",
                        cls="btn btn-outline-primary w-100 mb-2 py-2 fw-semibold",
                        onclick=f"""
                            window.addToQuoteBag({{
                                id: '{slug}',
                                name: '{name.replace("'", "")}',
                                price: '{price}',
                                priceNum: {clean_price_val or 0},
                                image: '{image}',
                                category: '{category_slug}'
                            }});
                            const modal = bootstrap.Modal.getInstance(document.getElementById('quickViewModal'));
                            if (modal) modal.hide();
                        """,
                    ),
                    A(
                        Icon("whatsapp", cls="me-2"), "Direct 1-Click Order",
                        href=whatsapp_url(direct_msg),
                        target="_blank", rel="noreferrer",
                        cls="btn btn-success w-100 py-2 fw-bold",
                    ),
                    cls="pt-3 border-top",
                ),
                cls="d-flex flex-column h-100 justify-content-between",
            ),
            md=6, cols=12,
        ),
        cls="g-4 align-items-center",
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
        skip_to_content_link(),
        Div(
            site_nav(current_path),
            Main(*sections, id="main-content", cls="site-main"),
            site_footer(),
            floating_whatsapp_button(),
            floating_quote_bag_button(),
            quote_bag_drawer(),
            product_quick_view_modal(),
            Script(f"""
                // Theme Toggle
                function toggleTheme() {{
                    const html = document.documentElement;
                    const current = html.getAttribute('data-bs-theme');
                    const next = current === 'dark' ? 'light' : 'dark';
                    html.setAttribute('data-bs-theme', next);
                    localStorage.setItem('sj-theme', next);
                }}
                (function() {{
                    const saved = localStorage.getItem('sj-theme');
                    if (saved) document.documentElement.setAttribute('data-bs-theme', saved);
                }})();

                // Quote Bag Runtime
                const WA_NUM = '{WHATSAPP_NUMBER}';
                window.getQuoteBag = function() {{
                    try {{
                        return JSON.parse(localStorage.getItem('sj_quote_bag') || '[]');
                    }} catch (e) {{
                        return [];
                    }}
                }};

                window.saveQuoteBag = function(bag) {{
                    localStorage.setItem('sj_quote_bag', JSON.stringify(bag));
                    window.renderQuoteBag();
                }};

                window.addToQuoteBag = function(item) {{
                    const bag = window.getQuoteBag();
                    const existing = bag.find(x => x.id === item.id);
                    if (existing) {{
                        existing.qty = (existing.qty || 1) + 1;
                    }} else {{
                        bag.push({{ ...item, qty: 1 }});
                    }}
                    window.saveQuoteBag(bag);
                    const toast = document.createElement('div');
                    toast.className = 'position-fixed bottom-0 start-50 translate-middle-x mb-4 p-3 bg-dark text-white rounded-pill shadow-lg';
                    toast.style.zIndex = '2000';
                    toast.innerHTML = '<i class="bi bi-bag-check-fill text-warning me-2"></i>Added <strong>' + item.name + '</strong> to WhatsApp Bag!';
                    document.body.appendChild(toast);
                    setTimeout(() => toast.remove(), 2500);
                }};

                window.updateBagQty = function(id, delta) {{
                    let bag = window.getQuoteBag();
                    const item = bag.find(x => x.id === id);
                    if (item) {{
                        item.qty = (item.qty || 1) + delta;
                        if (item.qty <= 0) {{
                            bag = bag.filter(x => x.id !== id);
                        }}
                    }}
                    window.saveQuoteBag(bag);
                }};

                window.clearQuoteBag = function() {{
                    window.saveQuoteBag([]);
                }};

                window.renderQuoteBag = function() {{
                    const bag = window.getQuoteBag();
                    const badge = document.getElementById('cart-item-count');
                    const totalCount = bag.reduce((sum, x) => sum + (x.qty || 1), 0);
                    if (badge) badge.innerText = totalCount;

                    const list = document.getElementById('quote-bag-items-list');
                    const subtotalEl = document.getElementById('quote-bag-subtotal');
                    if (!list) return;

                    if (bag.length === 0) {{
                        list.innerHTML = '<div class="text-center py-5 text-muted"><p class="mb-0">Your quote bag is empty.</p><small>Browse products and click "Add" to build your order.</small></div>';
                        if (subtotalEl) subtotalEl.innerText = 'NGN 0';
                        return;
                    }}

                    let subtotal = 0;
                    let html = '';
                    bag.forEach(item => {{
                        const qty = item.qty || 1;
                        const itemPrice = parseFloat(item.priceNum) || 0;
                        const lineTotal = itemPrice * qty;
                        subtotal += lineTotal;

                        html += `
                            <div class="d-flex align-items-center justify-content-between p-2 mb-2 bg-white rounded border">
                                <img src="${{item.image || ''}}" class="rounded me-2" style="width: 3.5rem; height: 3.5rem; object-fit: cover;">
                                <div class="flex-grow-1 me-2 overflow-hidden">
                                    <p class="fw-semibold mb-0 text-truncate small">${{item.name}}</p>
                                    <span class="text-muted small">${{item.price}}</span>
                                </div>
                                <div class="d-flex align-items-center gap-1">
                                    <button class="btn btn-sm btn-outline-secondary px-2 py-0" onclick="window.updateBagQty('${{item.id}}', -1)">-</button>
                                    <span class="fw-bold px-1 small">${{qty}}</span>
                                    <button class="btn btn-sm btn-outline-secondary px-2 py-0" onclick="window.updateBagQty('${{item.id}}', 1)">+</button>
                                </div>
                            </div>
                        `;
                    }});
                    list.innerHTML = html;
                    if (subtotalEl) {{
                        subtotalEl.innerText = 'NGN ' + subtotal.toLocaleString();
                    }}
                }};

                window.dispatchQuoteBagToWhatsApp = function() {{
                    const bag = window.getQuoteBag();
                    if (bag.length === 0) {{
                        alert('Your quote bag is empty.');
                        return;
                    }}
                    const name = document.getElementById('bag-customer-name')?.value.trim() || 'Client';
                    const phone = document.getElementById('bag-customer-phone')?.value.trim() || '';

                    let msg = `Hello SJ Interiors, my name is ${{name}}.\n`;
                    if (phone) msg += `Contact / City: ${{phone}}\n`;
                    msg += `\nI would like to place an order / quote for the following items:\n\n`;

                    let subtotal = 0;
                    bag.forEach((it, idx) => {{
                        const q = it.qty || 1;
                        const p = parseFloat(it.priceNum) || 0;
                        subtotal += (p * q);
                        msg += `${{idx + 1}}. ${{it.name}} (Qty: ${{q}}) — ${{it.price}}\n`;
                    }});

                    msg += `\nEstimated Total: NGN ${{subtotal.toLocaleString()}}\n`;
                    msg += `\nPlease confirm availability and delivery timeframe. Thank you!`;

                    const waUrl = 'https://wa.me/' + WA_NUM + '?text=' + encodeURIComponent(msg);
                    window.open(waUrl, '_blank');
                }};

                // Initialize on DOM load
                document.addEventListener('DOMContentLoaded', function() {{
                    window.renderQuoteBag();
                }});
            """),
            cls="site-app",
        ),
    )


def service_card(service: Any) -> Card:
    """Service card for the services listing page with mobile-friendly action buttons."""
    title = _value(service, "title", "Service")
    slug = _value(service, "slug", "")
    summary = _value(service, "summary", "")
    description = _value(service, "description", "")
    icon = _value(service, "icon", "stars")
    image = _value(service, "image_url", "")

    message = f"Hello SJ Interiors, I'm interested in your {title} service. I'd like to get an official quotation."

    card_body = Div(
        Div(Icon(icon), cls="service-icon mb-2 text-primary fs-3"),
        H3(title, cls="service-title fs-5 fw-bold text-dark mb-2"),
        P(summary, cls="service-summary small text-secondary mb-2"),
        P(description, cls="service-description small text-muted mb-3 flex-grow-1"),
        Div(
            A(
                Icon("whatsapp", cls="me-1"), "WhatsApp Quote",
                href=whatsapp_url(message),
                target="_blank",
                rel="noreferrer",
                cls="btn btn-success btn-sm w-100 fw-semibold",
            ),
            cls="mt-auto pt-3 border-top",
        ),
        cls="p-4 d-flex flex-column h-100",
    )

    if image:
        return Card(card_body, img_top=image, cls="service-card border-0 shadow-sm h-100 bg-white", body_cls="p-0 d-flex flex-column h-100")
    return Card(card_body, cls="service-card border-0 shadow-sm h-100 bg-white", body_cls="p-0 d-flex flex-column h-100")


def services_grid(services: list[Any]) -> Div:
    """Responsive 6-category service catalog with itemized deliverables."""
    categories = SERVICE_CATEGORIES
    cards = []
    for cat in categories:
        item_badges = [
            Div(
                Icon("check-circle-fill", cls="text-primary me-2 flex-shrink-0 small"),
                Div(
                    P(it["name"], cls="fw-semibold mb-0 small text-dark"),
                    Small(it["desc"], cls="text-muted"),
                ),
                cls="d-flex align-items-start py-1 border-bottom border-light",
            )
            for it in cat.items[:5]
        ]
        wa_msg = f"Hello SJ Interiors, I want an official quotation for '{cat.title}'."

        cards.append(
            Col(
                Card(
                    Img(src=cat.image, alt=cat.title, cls="card-img-top object-fit-cover", style="height: 14rem;"),
                    Div(
                        Div(
                            Badge(f"Division {cat.number:02d}", variant="light", cls="text-dark border me-2"),
                            cls="mb-2",
                        ),
                        H3(cat.title, cls="h5 fw-bold text-dark mb-2"),
                        P(cat.summary, cls="small text-secondary mb-3"),
                        Div(
                            P("Key Inclusions & Estimation Details:", cls="fw-bold small text-dark mb-2"),
                            Div(*item_badges, cls="mb-3"),
                            cls="bg-light p-3 rounded-3 mb-3",
                        ),
                        Div(
                            A(
                                Icon("whatsapp", cls="me-1"), "Request Official Quotation",
                                href=whatsapp_url(wa_msg),
                                target="_blank", rel="noreferrer",
                                cls="btn btn-success btn-sm w-100 fw-semibold text-white py-2",
                            ),
                            cls="mt-auto",
                        ),
                        cls="p-4 d-flex flex-column h-100",
                    ),
                    cls="border-0 shadow-sm h-100 bg-white",
                    body_cls="p-0 d-flex flex-column h-100",
                ),
                lg=4, md=6, cols=12, cls="mb-4",
            )
        )

    return Div(
        Row(*cards, cls="g-4", cols=1, cols_md=2, cols_lg=3),
        cls="services-grid",
    )


def service_inquiry_form() -> Form:
    """Interactive multi-category service planner & quote builder form."""
    categories = SERVICE_CATEGORIES

    category_boxes = []
    for cat in categories:
        category_boxes.append(
            Div(
                Div(
                    Input(
                        type="checkbox",
                        name="selected_services",
                        value=cat.id,
                        cls="form-check-input me-2",
                        id=f"cat-chk-{cat.id}",
                    ),
                    Label(
                        Div(
                            P(f"{cat.number}. {cat.title}", cls="fw-bold text-dark mb-0 small"),
                            Small(cat.summary, cls="text-muted"),
                        ),
                        fr=f"cat-chk-{cat.id}",
                        cls="form-check-label w-100",
                    ),
                    cls="form-check d-flex align-items-start p-3 border rounded-3 bg-white mb-2 shadow-xs",
                ),
                cls="col-md-6 mb-2",
            )
        )

    return Form(
        Div(
            H4("1. Select Service Categories Needed", cls="h5 fw-bold text-primary mb-2"),
            P("Tick all the areas that apply to your apartment, home, or commercial project:", cls="small text-muted mb-3"),
            Row(*category_boxes, cls="g-2 mb-4"),
            cls="mb-3",
        ),
        Hr(cls="my-4"),
        Div(
            H4("2. Project Scope & Room Details", cls="h5 fw-bold text-primary mb-2"),
            Row(
                Div(
                    Label("Apartment / Project Type", fr="inquiry-app-type", cls="form-label small fw-semibold"),
                    Select(
                        Option("Full Duplex / Mansion", value="duplex"),
                        Option("3-4 Bedroom Flat", value="3_4_bed"),
                        Option("1-2 Bedroom Apartment", value="1_2_bed"),
                        Option("Shortlet / Airbnb Apartment", value="shortlet"),
                        Option("Hotel / Commercial Suite", value="hotel"),
                        Option("Single Room Refresh", value="single_room"),
                        name="property_type", id="inquiry-app-type", cls="form-select form-select-sm",
                    ),
                    cls="col-md-6 mb-3",
                ),
                Div(
                    Label("Estimated Window Count", fr="inquiry-windows", cls="form-label small fw-semibold"),
                    Input(type="number", name="window_count", id="inquiry-windows", min="1", max="50",
                          placeholder="e.g. 5 windows", cls="form-control form-control-sm"),
                    cls="col-md-6 mb-3",
                ),
            ),
            Div(
                Label("Project Description & Specific Requirements", fr="inquiry-message", cls="form-label small fw-semibold"),
                Textarea(
                    name="message", id="inquiry-message", rows="3", cls="form-control form-control-sm",
                    placeholder="Provide details (e.g. Living room French pleat blackout curtains, 2 king beds, full kitchenware setup for shortlet, Ilorin delivery...)"
                ),
                cls="mb-3",
            ),
            cls="mb-3",
        ),
        Hr(cls="my-4"),
        Div(
            H4("3. Your Contact Details", cls="h5 fw-bold text-primary mb-2"),
            Row(
                Div(
                    Label("Full Name", fr="inquiry-name", cls="form-label small fw-semibold"),
                    Input(type="text", name="customer_name", id="inquiry-name", required=True,
                          cls="form-control form-control-sm", placeholder="e.g. Adebayo Olamide"),
                    cls="col-md-6 mb-3",
                ),
                Div(
                    Label("Phone Number (WhatsApp Active)", fr="inquiry-phone", cls="form-label small fw-semibold"),
                    Input(type="tel", name="phone", id="inquiry-phone", required=True,
                          cls="form-control form-control-sm", placeholder="e.g. 08026022672"),
                    cls="col-md-6 mb-3",
                ),
            ),
            Row(
                Div(
                    Label("Email Address (Optional)", fr="inquiry-email", cls="form-label small fw-semibold"),
                    Input(type="email", name="email", id="inquiry-email",
                          cls="form-control form-control-sm", placeholder="e.g. you@example.com"),
                    cls="col-md-6 mb-3",
                ),
                Div(
                    Label("Delivery City / State", fr="inquiry-city", cls="form-label small fw-semibold"),
                    Input(type="text", name="city", id="inquiry-city",
                          cls="form-control form-control-sm", placeholder="e.g. Ilorin, Kwara State"),
                    cls="col-md-6 mb-3",
                ),
            ),
            cls="mb-3",
        ),
        Div(
            Button(
                Icon("send-check", cls="me-2"), "Submit Service Request & Generate Lead",
                type="submit",
                cls="btn btn-primary w-100 py-3 fw-bold shadow-sm",
                hx_post="/services/inquiry",
                hx_target="#service-form-result",
                hx_swap="innerHTML",
            ),
            Div(id="service-form-result", cls="mt-3"),
            cls="mt-4",
        ),
        action="/services/inquiry",
        method="post",
        cls="service-inquiry-form p-4 bg-light rounded-4 border",
    )


def get_services_from_component() -> list[Any]:
    """Fetch services from the data layer (imported here to avoid circular imports)."""
    try:
        from .services import get_services as _get_services
    except ImportError:
        from services import get_services as _get_services
    return _get_services()


def how_it_works_section() -> Div:
    """Process steps section showing how SJ Interiors works with customers."""
    steps = [
        {"number": "01", "title": "Browse & Choose", "description": "Explore our services and select what fits your project."},
        {"number": "02", "title": "Send an Inquiry", "description": "Fill out the form or message us on WhatsApp with your requirements."},
        {"number": "03", "title": "Get a Quote", "description": "We'll respond within 2 hours with pricing and availability."},
        {"number": "04", "title": "Delivery & Styling", "description": "We handle delivery and can assist with installation and styling."},
    ]

    return Div(
        Container(
            section_intro(
                "How it works",
                "From inquiry to delivery in 4 simple steps",
                "We make it easy to get the interior products and services you need.",
                align="center",
            ),
            Row(
                *[
                    Col(
                        Card(
                            Div(Span(step["number"], cls="step-number"), cls="step-badge"),
                            H4(step["title"], cls="step-title"),
                            P(step["description"], cls="step-description"),
                            cls="step-card border-0 text-center h-100",
                            body_cls="p-4",
                        ),
                        lg=3,
                        md=6,
                        cols=12,
                        cls="mb-4",
                    )
                    for step in steps
                ],
                cls="g-4",
                cols=1,
                cols_md=2,
                cols_lg=4,
            ),
        ),
        cls="content-section content-section-soft",
    )


def empty_state(title: str, message: str, action_label: str = "", action_href: str = "") -> Div:
    """Reusable empty state component."""
    elements = [
        H3(title, cls="empty-state-title"),
        P(message, cls="empty-state-message"),
    ]
    if action_label and action_href:
        elements.append(Button(action_label, href=action_href, cls="btn btn-primary mt-3"))
    return Div(*elements, cls="text-center py-5 empty-state")


def loading_spinner() -> Div:
    """HTMX loading indicator."""
    return Div(
        Div(cls="spinner-border text-primary", role="status"),
        Span("Loading...", cls="visually-hidden"),
        cls="d-flex justify-content-center py-4",
        id="loading-spinner",
    )


def skip_to_content_link() -> A:
    """Skip-to-content accessibility link."""
    return A(
        "Skip to main content",
        href="#main-content",
        cls="sr-only sr-only-focusable",
    )


def toast_message(message: str, msg_type: str = "success") -> Div:
    """Toast notification for HTMX responses."""
    return Div(
        message,
        cls=f"alert alert-{msg_type} alert-dismissible fade show",
        role="alert",
        hx_swap_oob="true",
        id="toast-container",
    )


def contact_form() -> Div:
    """HTMX-powered contact form."""
    return Form(
        Div(
            Label("Your Name", fr="contact-name", cls="form-label"),
            Input(type="text", name="name", id="contact-name", required=True,
                  cls="form-control", placeholder="e.g. Adebayo Olamide"),
            cls="mb-3",
        ),
        Div(
            Label("Phone Number", fr="contact-phone", cls="form-label"),
            Input(type="tel", name="phone", id="contact-phone", required=True,
                  cls="form-control", placeholder="e.g. 08026022672"),
            cls="mb-3",
        ),
        Div(
            Label("Email", fr="contact-email", cls="form-label"),
            Input(type="email", name="email", id="contact-email", required=True,
                  cls="form-control", placeholder="e.g. you@example.com"),
            cls="mb-3",
        ),
        Div(
            Label("Message", fr="contact-message", cls="form-label"),
            Textarea(name="message", id="contact-message", rows="4", required=True,
                     cls="form-control", placeholder="How can we help you?"),
            cls="mb-3",
        ),
        Button(
            "Send Message",
            type="submit",
            cls="btn btn-primary px-4",
            hx_post="/contact/submit",
            hx_target="#contact-form-result",
            hx_swap="innerHTML",
        ),
        Div(id="contact-form-result", cls="mt-3"),
        action="/contact/submit",
        method="post",
        cls="contact-form",
    )


def order_lookup_form() -> Div:
    """Order lookup form for the order-lookup page."""
    return Form(
        Div(
            Label("Order Number", fr="order-number", cls="form-label"),
            Input(
                type="text",
                name="order_number",
                id="order-number",
                required=True,
                cls="form-control",
                placeholder="e.g. SJ-2026-0001",
            ),
            Small("Format: SJ-YYYY-NNNN", cls="form-text text-muted"),
            cls="mb-3",
        ),
        Button(
            "Track My Order",
            type="submit",
            cls="btn btn-primary px-4",
            hx_get="/order-lookup/result",
            hx_include="#order-number",
            hx_target="#order-result",
            hx_swap="innerHTML",
        ),
        Div(id="order-result", cls="mt-4"),
        method="get",
        cls="order-lookup-form",
    )


def order_status_result_card(order: dict | None, searched_num: str = "") -> Div:
    """Render customer-facing order status card with timeline."""
    if not order:
        return Div(
            Card(
                Div(
                    Icon("exclamation-circle", size="2.5rem", cls="text-warning mb-3"),
                    H4("Order Not Found", cls="mb-2"),
                    P(f"We could not locate an order matching '{searched_num}'. Please check the order number or contact our WhatsApp support team.", cls="text-muted small"),
                    A(
                        Icon("whatsapp", cls="me-2"), "Ask Support on WhatsApp",
                        href=whatsapp_url(f"Hello SJ Interiors, I'm checking on my order with reference '{searched_num}'."),
                        target="_blank", rel="noreferrer",
                        cls="btn btn-outline-success btn-sm mt-2",
                    ),
                    cls="p-4 text-center",
                ),
                cls="border-0 shadow-sm bg-light",
            )
        )

    order_num = order.get("order_number", searched_num)
    status = order.get("status", "processing").lower()
    cust_name = order.get("customer_name", "Valued Customer")
    items = order.get("items", []) or []

    status_steps = ["processing", "shipped", "delivered"]
    current_idx = status_steps.index(status) if status in status_steps else 0

    timeline_nodes = []
    for idx, step in enumerate(status_steps):
        is_done = idx <= current_idx
        is_current = idx == current_idx
        timeline_nodes.append(
            Div(
                Div(
                    Icon("check" if is_done else "circle", size="0.9rem"),
                    cls=f"rounded-circle d-flex align-items-center justify-content-center text-white {'bg-success' if is_done else 'bg-secondary'}",
                    style="width: 2rem; height: 2rem;",
                ),
                Span(step.title(), cls=f"small mt-1 {'fw-bold text-success' if is_current else 'text-muted'}"),
                cls="d-flex flex-column align-items-center flex-grow-1",
            )
        )

    items_list = []
    for it in items:
        if isinstance(it, dict):
            items_list.append(Li(f"{it.get('name', 'Item')} × {it.get('quantity', 1)} — {it.get('price', '')}", cls="small py-1"))
        elif isinstance(it, str):
            items_list.append(Li(it, cls="small py-1"))

    return Div(
        Card(
            Div(
                Div(
                    H3(f"Order {order_num}", cls="h5 fw-bold mb-0 text-primary"),
                    Badge(status.title(), variant={"processing": "warning", "shipped": "info", "delivered": "success", "cancelled": "danger"}.get(status, "secondary")),
                    cls="d-flex justify-content-between align-items-center mb-3",
                ),
                P(f"Customer: {cust_name}", cls="mb-3 text-muted small"),
                # Timeline
                Div(
                    *timeline_nodes,
                    cls="d-flex justify-content-between align-items-center my-4 py-2 border-top border-bottom bg-light rounded",
                ),
                items_list and Div(
                    P("Ordered Items:", cls="fw-semibold small mb-1"),
                    Ul(*items_list, cls="list-unstyled mb-3 ps-2 border-start border-2 border-primary"),
                ),
                Div(
                    A(
                        Icon("whatsapp", cls="me-1"), "Inquire on WhatsApp",
                        href=whatsapp_url(f"Hello SJ Interiors, I'm inquiring about the delivery timeline for Order {order_num}."),
                        target="_blank", rel="noreferrer",
                        cls="btn btn-outline-success btn-sm w-100",
                    ),
                    cls="mt-3",
                ),
                cls="p-4",
            ),
            cls="border-0 shadow-sm",
        )
    )

