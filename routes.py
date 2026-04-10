"""Route definitions for the SJ Interiors website."""

from __future__ import annotations

from typing import Any

from fasthtml.common import *
from starlette.responses import JSONResponse

from faststrap import Badge, Button, Card, Col, Container, Icon, Row

try:
    from .components import (
        featured_categories_section,
        hero_section,
        home_preview_section,
        lookbook_section,
        page_intro_banner,
        page_shell,
        product_grid,
        section_intro,
        shop_filter_bar,
        whatsapp_url,
        wholesale_cta_section,
    )
    from .content import (
        ADDRESS,
        BUSINESS_NAME,
        PHONE_NUMBERS,
        PHONE_NUMBER,
        PRODUCTS,
        SHORT_INTRO,
        SOCIALS,
        VALUE_POINTS,
        WHOLESALE_BENEFITS,
        category_label,
        products_for_category,
    )
except ImportError:
    from components import (
        featured_categories_section,
        hero_section,
        home_preview_section,
        lookbook_section,
        page_intro_banner,
        page_shell,
        product_grid,
        section_intro,
        shop_filter_bar,
        whatsapp_url,
        wholesale_cta_section,
    )
    from content import (
        ADDRESS,
        BUSINESS_NAME,
        PHONE_NUMBERS,
        PHONE_NUMBER,
        PRODUCTS,
        SHORT_INTRO,
        SOCIALS,
        VALUE_POINTS,
        WHOLESALE_BENEFITS,
        category_label,
        products_for_category,
    )


def home_page() -> tuple[Any, ...]:
    """Landing page content."""
    return (
        hero_section(),
        featured_categories_section(),
        home_preview_section(PRODUCTS),
        lookbook_section(),
        wholesale_cta_section(),
    )


def shop_page(category: str) -> tuple[Any, ...]:
    """Shop page content with category filtering."""
    all_categories = {product.category for product in PRODUCTS}
    active_category = category if category and category in all_categories else "all"
    filtered_products = products_for_category(active_category)
    category_name = "All Collections" if active_category == "all" else category_label(active_category)
    return (
        page_intro_banner(
            "Shop",
            "Browse SJ Interiors collections for bedrooms, windows, and soft finishing touches.",
            "From curtains and window blinds to bedsheets, duvets, pillows, and accessories, every item is easy to enquire about on WhatsApp.",
        ),
        Div(
            Container(
                Row(
                    Col(
                        section_intro(
                            "Browse the collection",
                            category_name,
                            "Filter by category to preview bedding, window treatments, pillows, and decor accessories.",
                            align="start",
                        ),
                        lg=7,
                        cols=12,
                    ),
                    Col(
                        Card(
                            Badge("Easy ordering", variant="warning", cls="mb-3"),
                            H3("Chat first, order fast.", cls="value-title"),
                            P(
                                "Once a customer spots something they like, the WhatsApp button can carry the product name straight into the conversation.",
                                cls="value-copy",
                            ),
                            cls="value-card border-0 h-100",
                            body_cls="p-4",
                        ),
                        lg=5,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-center g-4", cols=1, cols_md=2,
                ),
                Div(shop_filter_bar(active_category), cls="mt-4"),
                Div(product_grid(filtered_products), cls="mt-4"),
            ),
            cls="content-section",
        ),
        wholesale_cta_section(),
    )


def about_page() -> tuple[Any, ...]:
    """About page content."""
    story_cards = [
        Card(
            H3(title, cls="value-title"),
            P(copy, cls="value-copy"),
            cls="value-card border-0 h-100",
            body_cls="p-4",
        )
        for title, copy in VALUE_POINTS
    ]
    return (
        page_intro_banner(
            "About SJ Interiors",
            "Redefining your space through simplicity, comfort, and style.",
            SHORT_INTRO,
        ),
        Div(
            Container(
                Row(
                    Col(
                        Card(
                            Badge("Our story", variant="light", cls="mb-3"),
                            H2(
                                "We help rooms feel finished, welcoming, and easy to love.",
                                cls="section-title text-start",
                            ),
                            P(
                                "SJ Interiors brings together curtains, window blinds, bedsheets, duvets, pillows, "
                                "throw pillows, and accessories that help every room feel softer, cleaner, and more refined.",
                                cls="section-copy text-start mx-0",
                            ),
                            P(
                                "Whether you are refreshing a single room or sourcing for a larger project, the focus stays on practical comfort, stylish presentation, and dependable service.",
                                cls="section-copy text-start mx-0",
                            ),
                            cls="story-card border-0",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=7,
                        cols=12,
                    ),
                    Col(
                        Img(
                            src="https://images.unsplash.com/photo-1484101403633-562f891dc89a?auto=format&fit=crop&w=1400&q=80",
                            alt="Elegant bedroom setup with premium bedding and decor",
                            cls="about-image",
                            loading="lazy",
                        ),
                        lg=5,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-center g-4", cols=1, cols_md=2,
                ),
                Row(
                    *[Col(card, lg=4, cols=12, cls="mb-4") for card in story_cards],
                    cls="g-4 mt-4", cols=1, cols_lg=3
                ),
            ),
            cls="content-section",
        ),
        Div(
            Container(
                Row(
                    Col(
                        section_intro(
                            "How we serve",
                            "Retail ease with wholesale readiness.",
                            "We support one-room upgrades, home makeovers, apartment finishing, and larger supply requests with a simple ordering process.",
                            align="start",
                        ),
                        lg=5,
                        cols=12,
                    ),
                    Col(
                        Card(
                            *[
                                Div(
                                    Icon("check2-circle", cls="me-2"),
                                    Span(item),
                                    cls="cta-list-item",
                                )
                                for item in WHOLESALE_BENEFITS
                            ],
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=7,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-center g-4", cols=1, cols_md=2,
                ),
            ),
            cls="content-section content-section-soft",
        ),
        wholesale_cta_section(),
    )


def contact_page() -> tuple[Any, ...]:
    """Contact page content."""
    social_cards = [
        Card(
            Div(
                Icon(item["icon"], cls="contact-icon"),
                Div(
                    H3(item["label"], cls="value-title mb-1"),
                    P(item["handle"], cls="value-copy mb-0"),
                ),
                cls="d-flex align-items-center gap-3",
            ),
            footer=Button(
                "Open Profile",
                href=item["href"],
                target="_blank",
                rel="noreferrer",
                variant="light",
                cls="contact-link-btn",
            ),
            cls="value-card border-0 h-100",
            body_cls="p-4",
        )
        for item in SOCIALS
    ]
    return (
        page_intro_banner(
            "Contact",
            "Invite trust with a simple, direct ordering flow.",
            "Reach SJ Interiors quickly for enquiries, measurements, pricing, bulk requests, and order updates.",
        ),
        Div(
            Container(
                Row(
                    Col(
                        Card(
                            Badge("WhatsApp first", variant="warning", cls="mb-3"),
                            H2("Let us help you style your next order.", cls="section-title text-start"),
                            P(
                                "Send your product questions, preferred styles, and order requests directly on WhatsApp for a fast response.",
                                cls="section-copy text-start mx-0",
                            ),
                            Div(
                                Button(
                                    "Chat on WhatsApp",
                                    href=whatsapp_url(
                                        "Hello SJ Interiors, I want to make an inquiry about your bedding and decor collection."
                                    ),
                                    target="_blank",
                                    rel="noreferrer",
                                    cls="px-4",
                                ),
                                Button("Browse Shop", href="/shop", variant="light", cls="cta-light-btn"),
                                cls="d-flex flex-column flex-sm-row gap-3 mt-4",
                            ),
                            cls="story-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=7,
                        cols=12,
                    ),
                    Col(
                        Card(
                            Badge("Phone", variant="light", cls="mb-3"),
                            H3(PHONE_NUMBERS[0], cls="value-title"),
                            P(PHONE_NUMBERS[1], cls="value-copy mb-2"),
                            P(
                                ADDRESS,
                                cls="value-copy",
                            ),
                            P(
                                "Call or send a WhatsApp message for pricing, styling advice, bulk enquiries, and delivery information.",
                                cls="value-copy mb-0",
                            ),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=5,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-stretch g-4", cols=1, cols_md=2,
                ),
                Row(*[Col(card, lg=4, cols=12, cls="mb-4") for card in social_cards], cls="g-4 mt-4"),
                Row(
                    Col(
                        Card(
                            Badge("Customer support", variant="light", cls="mb-3"),
                            H3("What customers usually reach out for", cls="value-title"),
                            Div(
                                Div(Icon("check2-circle", cls="me-2"), Span("Curtains and window blind measurements"), cls="cta-list-item"),
                                Div(Icon("check2-circle", cls="me-2"), Span("Bedsheet, duvet, and pillow set recommendations"), cls="cta-list-item"),
                                Div(Icon("check2-circle", cls="me-2"), Span("Wholesale supply, delivery timelines, and availability"), cls="cta-list-item"),
                                cls="cta-list",
                            ),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=6,
                        cols=12,
                    ),
                    Col(
                        Img(
                            src="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1400&q=80",
                            alt="Styled interior decor accessories on a modern shelf",
                            cls="contact-image",
                            loading="lazy",
                        ),
                        lg=6,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-center g-4 mt-2", cols=1, cols_md=2,
                ),
            ),
            cls="content-section",
        ),
    )


def setup_site_routes(app: Any) -> None:
    """Register all app routes."""

    @app.get("/")
    def home() -> Any:
        return page_shell("Home", "/", *home_page())

    @app.get("/shop")
    def shop(category: str = "all") -> Any:
        return page_shell("Shop", "/shop", *shop_page(category))

    @app.get("/about")
    def about() -> Any:
        return page_shell("About", "/about", *about_page())

    @app.get("/contact")
    def contact() -> Any:
        return page_shell("Contact", "/contact", *contact_page())

    @app.get("/health")
    def health() -> JSONResponse:
        return JSONResponse(
            {"status": "healthy", "service": BUSINESS_NAME.lower().replace(" ", "-")}
        )
