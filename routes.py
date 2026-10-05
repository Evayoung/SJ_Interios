"""Route definitions for the SJ Interiors website."""

from __future__ import annotations

from typing import Any

from fasthtml.common import *
from starlette.requests import Request
from starlette.responses import JSONResponse

from faststrap import Badge, Button, Card, Col, Container, Icon, Row

import re
from urllib.parse import quote

try:
    from . import content
    from .components import (
        before_after_section,
        contact_form,
        empty_state,
        featured_categories_section,
        hero_section,
        home_preview_section,
        how_it_works_section,
        lookbook_section,
        order_lookup_form,
        order_status_result_card,
        page_intro_banner,
        page_shell,
        product_grid,
        quick_view_modal_fragment,
        section_intro,
        service_inquiry_form,
        services_grid,
        shop_filter_bar,
        shop_search_and_sort_bar,
        skip_to_content_link,
        testimonials_section,
        toast_message,
        whatsapp_url,
        wholesale_cta_section,
    )
    from .content import ADDRESS, BUSINESS_NAME, PHONE_NUMBERS, PHONE_NUMBER, TESTIMONIALS, TRANSFORMATIONS
    from .services import (
        get_brand_config,
        get_categories,
        get_category_label,
        get_category_slugs,
        get_featured_products,
        get_lookbook_items,
        get_order_by_number,
        get_products,
        get_services,
        get_testimonials,
        get_transformations,
        insert_client_feedback,
        insert_inquiry,
        insert_whatsapp_click,
    )
except Exception:
    import content
    from components import (
        before_after_section,
        contact_form,
        empty_state,
        featured_categories_section,
        hero_section,
        home_preview_section,
        how_it_works_section,
        lookbook_section,
        order_lookup_form,
        order_status_result_card,
        page_intro_banner,
        page_shell,
        product_grid,
        quick_view_modal_fragment,
        section_intro,
        service_inquiry_form,
        services_grid,
        shop_filter_bar,
        shop_search_and_sort_bar,
        skip_to_content_link,
        testimonials_section,
        toast_message,
        whatsapp_url,
        wholesale_cta_section,
    )
    from content import ADDRESS, BUSINESS_NAME, PHONE_NUMBERS, PHONE_NUMBER, TESTIMONIALS, TRANSFORMATIONS
    from services import (
        get_brand_config,
        get_categories,
        get_category_label,
        get_category_slugs,
        get_featured_products,
        get_lookbook_items,
        get_order_by_number,
        get_products,
        get_services,
        get_testimonials,
        get_transformations,
        insert_client_feedback,
        insert_inquiry,
        insert_whatsapp_click,
    )


# ──────────────────────────────────────────────
# Validation helpers
# ──────────────────────────────────────────────

NIGERIAN_PHONE = re.compile(r"^(\+?234|0)[789][01]\d{8}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def _validate_contact_form(name: str, phone: str, email: str, message: str) -> list[str]:
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")
    if not phone or not NIGERIAN_PHONE.match(phone.strip()):
        errors.append("Please enter a valid Nigerian phone number (e.g. 08026022672).")
    if not email or not EMAIL_REGEX.match(email.strip()):
        errors.append("Please enter a valid email address.")
    if not message or len(message.strip()) < 10:
        errors.append("Message must be at least 10 characters.")
    return errors


def home_page() -> tuple[Any, ...]:
    """Landing page content with dynamic data."""
    brand = get_brand_config()
    hero_slides = brand.get("hero_slides", [])
    featured_products = get_featured_products()
    transformations = get_transformations()
    testimonials = get_testimonials()
    return (
        hero_section(brand=brand, hero_slides=hero_slides),
        featured_categories_section(get_categories()),
        home_preview_section(featured_products),
        lookbook_section(),
        before_after_section(transformations=transformations),
        testimonials_section(testimonials=testimonials),
        wholesale_cta_section(brand=brand),
    )



def shop_page(category: str = "all", sort: str = "featured", q: str = "") -> tuple[Any, ...]:
    """Shop page content with category filtering, search, and sorting."""
    categories = get_categories()
    active_category = category if category and category in get_category_slugs() else "all"
    filtered_products = get_products(active_category)

    if q:
        q_lower = q.lower()
        filtered_products = [p for p in filtered_products if q_lower in _component_value(p, "name", "").lower() or q_lower in _component_value(p, "description", "").lower()]

    if sort == "price_asc":
        filtered_products = sorted(filtered_products, key=lambda p: float(str(_component_value(p, "price", "0")).replace("NGN", "").replace(",", "").strip() or 0))
    elif sort == "price_desc":
        filtered_products = sorted(filtered_products, key=lambda p: float(str(_component_value(p, "price", "0")).replace("NGN", "").replace(",", "").strip() or 0), reverse=True)
    elif sort == "name_asc":
        filtered_products = sorted(filtered_products, key=lambda p: _component_value(p, "name", "").lower())

    category_name = "All Collections" if active_category == "all" else get_category_label(active_category, categories)

    return (
        page_intro_banner(
            "Shop Collections",
            "Browse SJ Interiors collections for bedrooms, windows, and soft finishing touches.",
            "From curtains and window blinds to bedsheets, duvets, pillows, and accessories, every item is easy to enquire about on WhatsApp.",
        ),
        Div(
            Container(
                Row(
                    Col(
                        section_intro(
                            "Curated Storefront",
                            category_name,
                            "Filter by category, search fabrics & bedding, and add items to your WhatsApp Quote Bag.",
                            align="start",
                        ),
                        lg=7,
                        cols=12,
                    ),
                    Col(
                        Card(
                            Badge("Multi-Item Quote Bag", variant="warning", cls="mb-2"),
                            H3("Build your order in 1-click.", cls="value-title"),
                            P(
                                "Add multiple items to your Quote Bag and dispatch the complete list directly to WhatsApp in a single structured message.",
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
                Div(shop_search_and_sort_bar(active_category=active_category, active_sort=sort, query=q, categories=categories), cls="mt-4"),
                Div(product_grid(filtered_products), id="product-results-container", cls="mt-4"),
            ),
            cls="content-section",
        ),
        testimonials_section(),
        wholesale_cta_section(),
    )


def about_page() -> tuple[Any, ...]:
    """About page content."""
    brand = get_brand_config()
    story_cards = [
        Card(
            H3(title, cls="value-title"),
            P(copy, cls="value-copy"),
            cls="value-card border-0 h-100",
            body_cls="p-4",
        )
        for title, copy in brand.get("value_points", content.VALUE_POINTS)
    ]
    return (
        page_intro_banner(
            "About SJ Interiors",
            "Redefining your space through simplicity, comfort, and style.",
            brand.get(
                "about_subtitle",
                "Handcrafted drapery, custom bedding sets, and curated soft furnishings designed for modern Nigerian homes and hospitality spaces.",
            ),
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
                                brand.get(
                                    "about_copy",
                                    "SJ Interiors brings together curtains, window blinds, bedsheets, duvets, pillows, throw pillows, and accessories that help every room feel softer, cleaner, and more refined.",
                                ),
                                cls="section-copy text-start mx-0",
                            ),
                            P(
                                brand.get(
                                    "about_support",
                                    "Whether you are refreshing a single room or sourcing for a larger project, the focus stays on practical comfort, stylish presentation, and dependable service.",
                                ),
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
        before_after_section(),
        testimonials_section(),
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
                                for item in brand.get("wholesale_benefits", content.WHOLESALE_BENEFITS)
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
    brand = get_brand_config()
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
        for item in brand.get("socials", content.SOCIALS)
    ]
    return (
        page_intro_banner(
            "Contact Us",
            "Let's Bring Your Space to Life.",
            "Reach SJ Interiors directly for enquiries, bespoke measurements, fabric consultations, and order updates.",
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
                # Contact form section
                Row(
                    Col(
                        Card(
                            Badge("Send us a message", variant="light", cls="mb-3"),
                            H3("Or fill out this form", cls="value-title"),
                            P("We'll get back to you within 2 hours during business hours.", cls="value-copy mb-3"),
                            contact_form(),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=6,
                        cols=12,
                        cls="mt-4",
                    ),
                    Col(
                        empty_state("", "") if False else Div(),  # Placeholder
                        lg=6,
                        cols=12,
                        cls="mt-4",
                    ),
                    cls="align-items-start g-4 mt-2", cols=1, cols_md=2,
                ),
            ),
            cls="content-section",
        ),
    )


def services_page() -> tuple[Any, ...]:
    """Full services listing page with inquiry form."""
    services = get_services()
    return (
        page_intro_banner(
            "Our Services",
            "Professional interior styling, supply, and consultancy.",
            "From curtain design to complete room makeovers, SJ Interiors offers a full range of services for homes and businesses.",
        ),
        how_it_works_section(),
        Div(
            Container(
                services_grid(services) if services else empty_state(
                    "No services yet",
                    "We're setting up our service catalog. Check back soon!",
                    action_label="Browse Shop",
                    action_href="/shop",
                ),
            ),
            cls="content-section",
        ),
        Div(
            Container(
                Row(
                    Col(
                        section_intro(
                            "Get in touch",
                            "Tell us about your project",
                            "Select the services you're interested in and we'll reach out to discuss your needs.",
                            align="start",
                        ),
                        lg=5,
                        cols=12,
                    ),
                    Col(
                        Card(
                            service_inquiry_form(),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=7,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-start g-4", cols=1, cols_md=2,
                ),
            ),
            cls="content-section content-section-soft",
        ),
        wholesale_cta_section(),
    )


def order_lookup_page() -> tuple[Any, ...]:
    """Public order lookup page."""
    return (
        page_intro_banner(
            "Order Status",
            "Track your SJ Interiors order",
            "Enter your order number to check the current status of your order.",
        ),
        Div(
            Container(
                Row(
                    Col(
                        Card(
                            Badge("Order lookup", variant="light", cls="mb-3"),
                            H3("Enter your order number", cls="value-title"),
                            P("Your order number starts with SJ- followed by the year and sequence, e.g. SJ-2026-0001.", cls="value-copy mb-3"),
                            order_lookup_form(),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=6,
                        cols=12,
                    ),
                    Col(
                        Card(
                            Badge("Need help?", variant="warning", cls="mb-3"),
                            H3("Can't find your order?", cls="value-title"),
                            P("If you don't have your order number, reach out to us directly on WhatsApp with your name and phone number.", cls="value-copy"),
                            Button(
                                "Chat on WhatsApp",
                                href=whatsapp_url("Hello SJ Interiors, I need help tracking my order."),
                                target="_blank",
                                rel="noreferrer",
                                cls="mt-3 px-4",
                            ),
                            cls="value-card border-0 h-100",
                            body_cls="p-4 p-lg-5",
                        ),
                        lg=6,
                        cols=12,
                        cls="mt-4 mt-lg-0",
                    ),
                    cls="align-items-start g-4", cols=1, cols_md=2,
                ),
            ),
            cls="content-section",
        ),
    )


def setup_site_routes(app: Any) -> None:
    """Register all app routes."""

    # ── Page routes ──────────────────────────────────────────────

    @app.get("/")
    def home() -> Any:
        return page_shell("Home", "/", *home_page())

    @app.get("/shop")
    def shop(category: str = "all", sort: str = "featured", q: str = "") -> Any:
        return page_shell("Shop", "/shop", *shop_page(category=category, sort=sort, q=q))

    @app.get("/about")
    def about() -> Any:
        return page_shell("About", "/about", *about_page())

    @app.get("/contact")
    def contact() -> Any:
        return page_shell("Contact", "/contact", *contact_page())

    @app.get("/services")
    def services() -> Any:
        return page_shell("Services", "/services", *services_page())

    @app.get("/order-lookup")
    def order_lookup() -> Any:
        return page_shell("Order Lookup", "/order-lookup", *order_lookup_page())

    @app.get("/health")
    def health() -> JSONResponse:
        return JSONResponse(
            {"status": "healthy", "service": BUSINESS_NAME.lower().replace(" ", "-")}
        )

    # ── HTMX fragment endpoints ─────────────────────────────────

    @app.get("/shop/product-modal/{slug}")
    def shop_product_modal(slug: str) -> Any:
        """HTMX: return rich quick-view modal fragment."""
        all_prods = get_products("all")
        matched = next((p for p in all_prods if _component_value(p, "slug", _component_value(p, "name", "").lower().replace(" ", "-")) == slug), None)
        if not matched:
            # Fallback search by name
            matched = next((p for p in all_prods if slug.replace("-", " ") in _component_value(p, "name", "").lower()), None)
        return quick_view_modal_fragment(matched)

    @app.get("/shop/results")
    def shop_results(category: str = "all", sort: str = "featured", q: str = "") -> Any:
        """HTMX: return filtered, searched, and sorted product grid."""
        active_category = category if category in get_category_slugs() else "all"
        filtered = get_products(active_category)

        if q:
            q_lower = q.lower().strip()
            filtered = [
                p for p in filtered
                if q_lower in _component_value(p, "name", "").lower()
                or q_lower in _component_value(p, "description", "").lower()
                or q_lower in _component_value(p, "highlight", "").lower()
            ]

        if sort == "price_asc":
            filtered = sorted(filtered, key=lambda p: float(str(_component_value(p, "price", "0")).replace("NGN", "").replace(",", "").strip() or 0))
        elif sort == "price_desc":
            filtered = sorted(filtered, key=lambda p: float(str(_component_value(p, "price", "0")).replace("NGN", "").replace(",", "").strip() or 0), reverse=True)
        elif sort == "name_asc":
            filtered = sorted(filtered, key=lambda p: _component_value(p, "name", "").lower())

        return product_grid(filtered)

    @app.get("/shop/filter")
    def shop_filter(category: str = "all") -> Any:
        """HTMX: return filtered product grid fragment."""
        return shop_results(category=category)

    @app.get("/shop/search")
    def shop_search(q: str = "") -> Any:
        """HTMX: return filtered product grid for live search."""
        return shop_results(q=q)

    @app.post("/contact/submit")
    def contact_submit(name: str, phone: str, email: str, message: str) -> Any:
        """HTMX: handle contact form submission."""
        errors = _validate_contact_form(name, phone, email, message)
        if errors:
            return Div(
                *[
                    P(err, cls="alert alert-danger mb-1")
                    for err in errors
                ],
                id="contact-form-result",
            )

        result = insert_inquiry(
            customer_name=name.strip(),
            phone=phone.strip(),
            email=email.strip(),
            message=message.strip(),
            source="contact_form",
        )

        if result:
            return Div(
                P("Thank you! We've received your message and will respond within 2 hours.",
                  cls="alert alert-success"),
                id="contact-form-result",
            )
        return Div(
            P("Thank you! Your message has been noted. We'll be in touch soon.",
              cls="alert alert-info"),
            id="contact-form-result",
        )

    @app.post("/services/inquiry")
    async def service_inquiry_submit(req: Request) -> Any:
        """HTMX: handle rich multi-category service inquiry form submission."""
        form = await req.form()
        customer_name = str(form.get("customer_name", "")).strip()
        phone = str(form.get("phone", "")).strip()
        email = str(form.get("email", "")).strip()
        message = str(form.get("message", "")).strip()
        property_type = str(form.get("property_type", "Standard"))
        window_count = str(form.get("window_count", ""))
        city = str(form.get("city", "")).strip()
        selected_services = form.getlist("selected_services")

        real_errors = []
        if not customer_name or len(customer_name) < 2:
            real_errors.append("Name must be at least 2 characters.")
        if not phone or not NIGERIAN_PHONE.match(phone):
            real_errors.append("Please enter a valid Nigerian phone number (e.g. 08026022672).")

        if real_errors:
            return Div(
                *[P(err, cls="alert alert-danger mb-1") for err in real_errors],
                id="service-form-result",
            )

        # Build comprehensive project scope message
        scope_details = []
        if property_type:
            scope_details.append(f"Property Type: {property_type.replace('_', ' ').title()}")
        if window_count:
            scope_details.append(f"Estimated Windows: {window_count}")
        if city:
            scope_details.append(f"Location: {city}")
        if message:
            scope_details.append(f"Notes: {message}")

        full_message = " | ".join(scope_details) if scope_details else "Service request"

        result = insert_inquiry(
            customer_name=customer_name,
            phone=phone,
            email=email,
            message=full_message,
            source="services_page",
            selected_services=selected_services,
            service_inquiry=True,
        )

        wa_followup = quote(f"Hello SJ Interiors, I just submitted an official service request for {', '.join(selected_services) if selected_services else 'Interior Decoration'}. My name is {customer_name}.")

        return Div(
            Card(
                Div(
                    Icon("check-circle-fill", size="2rem", cls="text-success mb-2"),
                    H4("Service Request Received!", cls="h5 fw-bold text-success mb-2"),
                    P("Your project details have been sent to our design and estimation team. We will prepare your official proposal/quotation promptly.", cls="small text-muted mb-3"),
                    A(
                        Icon("whatsapp", cls="me-1"), "Follow Up Immediately on WhatsApp",
                        href=f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_followup}",
                        target="_blank", rel="noreferrer",
                        cls="btn btn-success btn-sm fw-bold",
                    ),
                    cls="p-3 text-center",
                ),
                cls="border border-success bg-white shadow-sm",
            ),
            id="service-form-result",
        )

    @app.get("/track/whatsapp-click")
    def track_whatsapp_click(product_id: str = "") -> JSONResponse:
        """Log a WhatsApp button click (fire-and-forget from HTMX)."""
        insert_whatsapp_click(product_id=product_id or None)
        return JSONResponse({"status": "ok"})

    @app.get("/order-lookup/result")
    def order_lookup_result(order_number: str = "") -> Any:
        """HTMX: return order status fragment."""
        if not order_number or not order_number.strip():
            return empty_state("Missing order number", "Please enter your order number to look up status.")

        order = get_order_by_number(order_number.strip())
        return order_status_result_card(order, searched_num=order_number.strip())

    @app.get("/feedback")
    def feedback_portal(req: Request) -> Any:
        """Public feedback & service complaints submission portal."""
        return (
            Title("Client Feedback & Support | SJ Interiors"),
            page_intro_banner(
                "Client Feedback & Support",
                "Your Feedback Shapes Our Craft.",
                "Share your honest styling review or request immediate assistance with your drapery, bedding, or styling project.",
            ),
            Style("""
                .feedback-tab-card {
                    background: #ffffff;
                    border: 1px solid rgba(110, 69, 201, 0.1);
                    border-radius: 1.25rem;
                }
                .feedback-nav-wrap {
                    display: flex;
                    gap: 0.5rem;
                    padding: 0.4rem;
                    background: #f8fafc;
                    border-radius: 9999px;
                    border: 1px solid #e2e8f0;
                    overflow-x: auto;
                    overflow-y: hidden;
                    scrollbar-width: none;
                    -ms-overflow-style: none;
                }
                .feedback-nav-wrap::-webkit-scrollbar {
                    display: none;
                }
                .feedback-nav-tab {
                    flex: 0 0 auto;
                    white-space: nowrap;
                    text-align: center;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.4rem;
                    padding: 0.55rem 1.1rem;
                    font-size: 0.88rem;
                    font-weight: 600;
                    border-radius: 9999px;
                    color: #4b5563;
                    background: transparent;
                    border: none;
                    text-decoration: none;
                    transition: all 0.2s ease-in-out;
                    cursor: pointer;
                }
                .feedback-nav-tab:hover {
                    color: #6E45C9;
                    background: rgba(110, 69, 201, 0.08);
                }
                .feedback-nav-tab.active[href="#tab-review"] {
                    background: #6E45C9 !important;
                    color: #ffffff !important;
                    box-shadow: 0 4px 14px rgba(110, 69, 201, 0.3) !important;
                }
                .feedback-nav-tab.active[href="#tab-complaint"] {
                    background: #c8607d !important;
                    color: #ffffff !important;
                    box-shadow: 0 4px 14px rgba(200, 96, 125, 0.3) !important;
                }
                .btn-brand-primary {
                    background-color: #6E45C9;
                    border-color: #6E45C9;
                    color: #ffffff;
                    transition: all 0.2s ease-in-out;
                }
                .btn-brand-primary:hover {
                    background-color: #5b35ad;
                    border-color: #5b35ad;
                    color: #ffffff;
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(110, 69, 201, 0.25);
                }
                .btn-brand-berry {
                    background-color: #c8607d;
                    border-color: #c8607d;
                    color: #ffffff;
                    transition: all 0.2s ease-in-out;
                }
                .btn-brand-berry:hover {
                    background-color: #b54f6c;
                    border-color: #b54f6c;
                    color: #ffffff;
                    transform: translateY(-1px);
                    box-shadow: 0 6px 16px rgba(200, 96, 125, 0.25);
                }
            """),
            Script("""
                (function() {
                    function initFeedbackTabs() {
                        var nav = document.getElementById('feedback-tab-nav');
                        if (!nav) return;
                        var tabs = nav.querySelectorAll('a.feedback-nav-tab');
                        tabs.forEach(function(tab) {
                            tab.addEventListener('click', function(e) {
                                e.preventDefault();
                                var target = this.getAttribute('href');
                                // Deactivate all tabs
                                tabs.forEach(function(t) {
                                    t.classList.remove('active');
                                    t.setAttribute('aria-selected', 'false');
                                });
                                // Activate clicked tab
                                this.classList.add('active');
                                this.setAttribute('aria-selected', 'true');
                                // Hide all panes
                                var panes = document.querySelectorAll('.tab-content .tab-pane');
                                panes.forEach(function(pane) {
                                    pane.classList.remove('show', 'active');
                                });
                                // Show target pane
                                var targetPane = document.querySelector(target);
                                if (targetPane) {
                                    targetPane.classList.add('show', 'active');
                                }
                            });
                        });
                    }
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', initFeedbackTabs);
                    } else {
                        initFeedbackTabs();
                    }
                })();
            """),
            Container(
                Row(
                    Col(
                        Card(
                            Div(
                                Ul(
                                    Li(A(Icon("star-fill", cls="me-2 text-warning"), "Write a Review", href="#tab-review", cls="feedback-nav-tab active", role="tab", aria_selected="true"), cls="nav-item"),
                                    Li(A(Icon("exclamation-circle-fill", cls="me-2 text-danger"), "Report a Complaint", href="#tab-complaint", cls="feedback-nav-tab", role="tab", aria_selected="false"), cls="nav-item"),
                                    cls="feedback-nav-wrap mb-4 list-unstyled",
                                    id="feedback-tab-nav",
                                ),
                                Div(id="feedback-result"),
                                Div(
                                    # Tab 1: Review Form
                                    Div(
                                        Form(
                                            Input(type="hidden", name="kind", value="review"),
                                            Row(
                                                Col(
                                                    Label("Your Full Name *", cls="form-label small fw-bold text-dark"),
                                                    Input(type="text", name="customer_name", placeholder="e.g. Mrs. Folashade Adeyemi", required=True, cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                                Col(
                                                    Label("WhatsApp / Phone Number *", cls="form-label small fw-bold text-dark"),
                                                    Input(type="tel", name="customer_phone", placeholder="e.g. 08026022672", required=True, cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                            ),
                                            Row(
                                                Col(
                                                    Label("Location / Neighborhood", cls="form-label small fw-bold text-dark"),
                                                    Input(type="text", name="location_tag", placeholder="e.g. GRA Ilorin, Kwara State", cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                                Col(
                                                    Label("Project / Product Category", cls="form-label small fw-bold text-dark"),
                                                    Select(
                                                        Option("Living Room Curtains & Drapery", value="Living Room Curtains"),
                                                        Option("Luxury Bedding & Duvet Sets", value="Luxury Bedding Sets"),
                                                        Option("Window Blinds (Day & Night / Roman)", value="Window Blinds"),
                                                        Option("Full House Interior Dressing", value="Full House Styling"),
                                                        Option("Hospitality / Hotel Bulk Order", value="Bulk Order"),
                                                        Option("Throw Pillows & Soft Furnishings", value="Throw Pillows & Decor"),
                                                        name="project_category", cls="form-select mb-3",
                                                    ),
                                                    span=12, md=6,
                                                ),
                                            ),
                                            Div(
                                                Label("Your Rating *", cls="form-label small fw-bold text-dark"),
                                                Select(
                                                    Option("5 Stars — Outstanding (Highly Recommended)", value="5", selected=True),
                                                    Option("4 Stars — Very Good Experience", value="4"),
                                                    Option("3 Stars — Satisfactory Service", value="3"),
                                                    Option("2 Stars — Needs Improvement", value="2"),
                                                    Option("1 Star — Unsatisfactory", value="1"),
                                                    name="rating", cls="form-select mb-3",
                                                ),
                                            ),
                                            Div(
                                                Label("Your Testimonial / Experience *", cls="form-label small fw-bold text-dark"),
                                                Textarea(
                                                    rows="4", name="message", required=True,
                                                    placeholder="Tell us about the craftsmanship, fabric quality, and how the team styled your space...",
                                                    cls="form-control mb-4",
                                                ),
                                            ),
                                            Button(
                                                Span(Icon("check-circle-fill", cls="me-2"), "Submit Review for Website"),
                                                type="submit", cls="btn btn-brand-primary px-4 py-3 fw-bold w-100",
                                                hx_post="/feedback/submit",
                                                hx_include="closest form",
                                                hx_target="#feedback-result",
                                                hx_swap="innerHTML",
                                                hx_disabled_elt="this",
                                            ),
                                            action="/feedback/submit", method="post",
                                        ),
                                        id="tab-review", cls="tab-pane fade show active",
                                    ),
                                    # Tab 2: Complaint Form
                                    Div(
                                        Form(
                                            Input(type="hidden", name="kind", value="complaint"),
                                            Row(
                                                Col(
                                                    Label("Your Full Name *", cls="form-label small fw-bold text-dark"),
                                                    Input(type="text", name="customer_name", placeholder="e.g. Alhaji Ibrahim Sani", required=True, cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                                Col(
                                                    Label("WhatsApp / Phone Number *", cls="form-label small fw-bold text-dark"),
                                                    Input(type="tel", name="customer_phone", placeholder="e.g. 08182233445", required=True, cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                            ),
                                            Row(
                                                Col(
                                                    Label("Order or Receipt Reference No. (if available)", cls="form-label small fw-bold text-dark"),
                                                    Input(type="text", name="order_ref", placeholder="e.g. REC-2026-0088 or INV-2026-0105", cls="form-control mb-3"),
                                                    span=12, md=6,
                                                ),
                                                Col(
                                                    Label("Issue Category *", cls="form-label small fw-bold text-dark"),
                                                    Select(
                                                        Option("Measurement Adjustment Needed", value="Measurement Adjustment"),
                                                        Option("Delivery / Dispatch Inquiry", value="Delivery Inquiry"),
                                                        Option("Installation Assistance Required", value="Installation Assistance"),
                                                        Option("Fabric / Tailoring Quality Concern", value="Quality Concern"),
                                                        Option("General Service Support", value="General Support"),
                                                        name="complaint_type", cls="form-select mb-3",
                                                    ),
                                                    span=12, md=6,
                                                ),
                                            ),
                                            Div(
                                                Label("Urgency Level", cls="form-label small fw-bold text-dark"),
                                                Select(
                                                    Option("Normal (Resolve within 48 hours)", value="normal", selected=True),
                                                    Option("Urgent (Resolve within 24 hours)", value="urgent"),
                                                    Option("Priority (Immediate Sister Attention)", value="priority"),
                                                    name="urgency", cls="form-select mb-3",
                                                ),
                                            ),
                                            Div(
                                                Label("Detailed Description of the Issue *", cls="form-label small fw-bold text-dark"),
                                                Textarea(
                                                    rows="4", name="message", required=True,
                                                    placeholder="Please provide full details so Sister Mercy and Christianah can review and assign immediate support...",
                                                    cls="form-control mb-4",
                                                ),
                                            ),
                                            Button(
                                                Span(Icon("send", cls="me-2"), "Submit Support Ticket to Co-Owners"),
                                                type="submit", cls="btn btn-brand-berry px-4 py-3 fw-bold w-100",
                                                hx_post="/feedback/submit",
                                                hx_include="closest form",
                                                hx_target="#feedback-result",
                                                hx_swap="innerHTML",
                                                hx_disabled_elt="this",
                                            ),
                                            action="/feedback/submit", method="post",
                                        ),
                                        id="tab-complaint", cls="tab-pane fade",
                                    ),
                                    cls="tab-content",
                                ),
                                cls="p-4 p-md-5",
                            ),
                            cls="feedback-tab-card shadow-sm mb-5",
                        ),
                        span=12, lg=10, cls="mx-auto",
                    ),
                    cls="justify-content-center",
                ),
            ),
        )


    @app.post("/feedback/submit")
    async def feedback_submit(req: Request) -> Any:
        """Handle submission of review or complaint."""
        form = await req.form()
        kind = form.get("kind", "review")
        name = form.get("customer_name", "Valued Client")
        phone = form.get("customer_phone", "")
        message = form.get("message", "")

        if not message.strip():
            return Div(
                Badge("Error", variant="danger", cls="me-2"),
                "Please provide a description or review message before submitting.",
                cls="alert alert-danger mb-4",
            )

        data = {
            "kind": kind,
            "customer_name": name,
            "customer_phone": phone,
            "customer_email": form.get("customer_email", ""),
            "rating": form.get("rating", 5),
            "project_category": form.get("project_category", "Interior Furnishing"),
            "location_tag": form.get("location_tag", "Ilorin"),
            "message": message,
            "order_ref": form.get("order_ref", ""),
            "complaint_type": form.get("complaint_type", "General"),
            "urgency": form.get("urgency", "normal"),
        }

        entry = insert_client_feedback(data)
        wa_num = whatsapp_url(f"Hello SJ Interiors, I just submitted a {kind} on your feedback portal. Customer: {name}")

        if kind == "review":
            return Div(
                Div(
                    Icon("check-circle-fill", size="2.5rem", cls="text-success mb-3"),
                    H4("Thank You for Sharing Your Experience!", cls="fw-bold text-dark"),
                    P(f"Dear {name}, your review has been submitted directly to Sister Mercy and Christianah. Once approved by our team, it will be published to the SJ Interiors website testimonials carousel.", cls="text-muted small mb-4"),
                    A(Icon("arrow-left", cls="me-1"), "Return to Homepage", href="/", cls="btn btn-outline-primary btn-sm me-2"),
                    A(Icon("bag", cls="me-1"), "Browse Featured Shop", href="/shop", cls="btn btn-primary btn-sm"),
                    cls="text-center p-4",
                ),
                cls="alert alert-success border-success rounded-4 bg-white shadow-sm mb-4",
            )
        else:
            return Div(
                Div(
                    Icon("shield-check", size="2.5rem", cls="text-danger mb-3"),
                    H4("Service Ticket Logged Successfully", cls="fw-bold text-dark"),
                    P(f"Dear {name}, your service ticket (Ref: {entry.get('id')}) has been received. Co-owners Mercy Olorundare and Christianah Alade have been notified to review your case and follow up with prompt resolution.", cls="text-muted small mb-3"),
                    A(Icon("whatsapp", cls="me-1"), "Follow Up Directly on WhatsApp", href=wa_num, target="_blank", rel="noreferrer", cls="btn btn-success btn-sm fw-bold"),
                    cls="text-center p-4",
                ),
                cls="alert alert-warning border-warning rounded-4 bg-white shadow-sm mb-4",
            )



def _component_value(item: Any, key: str, fallback: Any = None) -> Any:
    """Dual-mode value accessor for dicts and dataclasses."""
    if isinstance(item, dict):
        return item.get(key, fallback)
    return getattr(item, key, fallback)

