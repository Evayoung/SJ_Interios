"""Content and sample data for the SJ Interiors website."""

from __future__ import annotations

from dataclasses import dataclass

BUSINESS_NAME = "SJ Interiors"
BUSINESS_SUBTITLE = "Deco and Beddings"
TAGLINE = "Redefining your space with simplicity, comfort, and style."
SHORT_INTRO = (
    "SJ Interiors curates curtains, window blinds, bedsheets, duvets, pillows, and soft decor "
    "essentials that make homes feel calm, stylish, and beautifully put together."
)

WHATSAPP_NUMBER = "2348026022672"
PHONE_NUMBER = "+234 (911) 507-6282"
PHONE_NUMBERS = ["08026022672", "09115076282"]
ADDRESS = "Limca Junction Shopping Complex, Along Asa Dam Road, Ilorin, Kwara State"
LOCATION_SHORT = "Ilorin, Kwara State"


@dataclass(frozen=True)
class HeroSlide:
    image: str
    alt: str


@dataclass(frozen=True)
class Category:
    slug: str
    label: str
    description: str
    icon: str
    image: str


@dataclass(frozen=True)
class Product:
    name: str
    category: str
    price: str
    description: str
    image: str
    highlight: str


HERO_SLIDES = [
    HeroSlide(
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1600&q=80",
        alt="Modern bedroom styled with plush bedsheets and layered pillows",
    ),
    HeroSlide(
        image="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1600&q=80",
        alt="Elegant room with curtains and layered bedding",
    ),
    HeroSlide(
        image="https://images.unsplash.com/photo-1464890100898-a385f744067f?auto=format&fit=crop&w=1200&q=80",
        alt="Layered bed with duvet textures and soft interior styling",
    ),
    HeroSlide(
        image="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1600&q=80",
        alt="Bright interior decor styling with accessories and soft accents",
    ),
]

CATEGORIES = [
    Category(
        slug="bedsheets",
        label="Bedsheets",
        description="Soft, polished sheet sets for restful and photo-ready bedrooms.",
        icon="stars",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
    ),
    Category(
        slug="duvets",
        label="Duvets",
        description="Layered warmth with plush finishes and premium everyday comfort.",
        icon="moon-stars",
        image="https://images.unsplash.com/photo-1464890100898-a385f744067f?auto=format&fit=crop&w=1200&q=80",
    ),
    Category(
        slug="curtains",
        label="Curtains",
        description="Elegant drapes that soften light and elevate your interior story.",
        icon="layout-sidebar-inset",
        image="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
    ),
    Category(
        slug="pillows",
        label="Throw Pillows",
        description="Textured accents and rich tones for beds, sofas, and cozy corners.",
        icon="circle-square",
        image="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80",
    ),
    Category(
        slug="blinds",
        label="Window Blinds",
        description="Clean lines and practical privacy for modern home styling.",
        icon="border-all",
        image="https://images.unsplash.com/photo-1519643381401-22c77e60520e?auto=format&fit=crop&w=1200&q=80",
    ),
    Category(
        slug="decor",
        label="Throw Pillows & Accessories",
        description="Throw pillows and finishing accents that add softness and personality to your space.",
        icon="gem",
        image="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1200&q=80",
    ),
]

PRODUCTS = [
    Product(
        name="Signature Stripe Bedsheet Set",
        category="bedsheets",
        price="NGN 24,500",
        description="A smooth cotton blend set designed for crisp, hotel-inspired bedrooms.",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1000&q=80",
        highlight="Retail & wholesale",
    ),
    Product(
        name="Hotel White Bedsheet Bundle",
        category="bedsheets",
        price="NGN 32,000",
        description="Bright layered whites for guest rooms, rentals, and premium home styling.",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1000&q=80",
        highlight="Best for hospitality orders",
    ),
    Product(
        name="Layered Luxe Duvet",
        category="duvets",
        price="NGN 38,000",
        description="Soft volume and a smooth finish that instantly upgrades your bedscape.",
        image="https://images.unsplash.com/photo-1464890100898-a385f744067f?auto=format&fit=crop&w=1000&q=80",
        highlight="Soft touch finish",
    ),
    Product(
        name="Cozy Winter Duvet Duo",
        category="duvets",
        price="NGN 45,000",
        description="A fuller duvet pairing for homes that want extra comfort and layering.",
        image="https://images.unsplash.com/photo-1464890100898-a385f744067f?auto=format&fit=crop&w=1200&q=80",
        highlight="Luxury layered comfort",
    ),
    Product(
        name="Soft Sheer Curtain Pair", 
        category="curtains",
        price="NGN 28,500",
        description="Light-filtering curtains that keep spaces airy, bright, and elegant.",
        image="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1000&q=80",
        highlight="Made for bright interiors",
    ),
    Product(
        name="Pleated Blackout Curtain Set",
        category="curtains",
        price="NGN 34,000",
        description="Structured folds and rich drape weight for polished, private rooms.",
        image="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1000&q=80",
        highlight="Popular window upgrade",
    ),
    Product(
        name="Daylight Window Blinds",
        category="blinds",
        price="NGN 42,000",
        description="Modern blinds with a neat finish for offices, homes, and compact spaces.",
        image="https://images.unsplash.com/photo-1519643381401-22c77e60520e?auto=format&fit=crop&w=1000&q=80",
        highlight="Clean and practical",
    ),
    Product(
        name="Wooden Venetian Blind",
        category="blinds",
        price="NGN 49,000",
        description="Warm wooden texture for interiors that need privacy with character.",
        image="https://images.unsplash.com/photo-1519643381401-22c77e60520e?auto=format&fit=crop&w=1000&q=80",
        highlight="Premium window styling",
    ),
    Product(
        name="Velvet Throw Pillow Pair",
        category="pillows",
        price="NGN 18,000",
        description="Rich jewel tones with soft texture to complete sofas and bedding looks.",
        image="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1000&q=80",
        highlight="Easy styling accent",
    ),
    Product(
        name="Textured Cushion Trio",
        category="pillows",
        price="NGN 21,000",
        description="Mix-and-match patterned pillows for cozy, balanced interior styling.",
        image="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1000&q=80",
        highlight="Sofa and bed ready",
    ),
    Product(
        name="Gold Accent Wall Mirror",
        category="decor",
        price="NGN 35,500",
        description="A refined decorative mirror that adds light, glow, and visual depth.",
        image="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1000&q=80",
        highlight="Soft gold detail",
    ),
    Product(
        name="Decorative Tray & Vase Set",
        category="decor",
        price="NGN 27,500",
        description="A simple finishing set for consoles, dressers, and styled shelves.",
        image="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1000&q=80",
        highlight="Perfect finishing touch",
    ),
]

VALUE_POINTS = [
    (
        "Simplicity in every detail",
        "We bring together pieces that feel easy to style, easy to live with, and easy to love.",
    ),
    (
        "Comfort for everyday living",
        "From restful bedrooms to polished windows, we focus on softness, warmth, and visual balance.",
    ),
    (
        "Retail and wholesale supply",
        "We serve both individual buyers and larger requests for apartments, hospitality spaces, and resellers.",
    ),
]

WHOLESALE_BENEFITS = [
    "Curtains, blinds, bedding, and soft accessories supplied for both personal and bulk orders.",
    "Helpful recommendations for matching products across bedrooms, windows, and lounge spaces.",
    "Quick response on WhatsApp for enquiries, pricing, and order confirmation.",
]

SOCIALS = [
    {
        "label": "Instagram",
        "handle": "@sj_interior_deco_and_beddings",
        "href": "https://www.instagram.com/sj_interior_deco_and_beddings?igsh=YmU4ZTgwaDZlMmxz",
        "icon": "instagram",
    },
    {
        "label": "TikTok",
        "handle": "@sj_interior5",
        "href": "https://www.tiktok.com/@sj_interior5?_r=1&_t=ZS-94oz6j5vErV",
        "icon": "tiktok",
    },
]


def category_label(category_slug: str) -> str:
    """Return a human-friendly category label."""
    for category in CATEGORIES:
        if category.slug == category_slug:
            return category.label
    return "All Collections"


def products_for_category(category_slug: str | None) -> list[Product]:
    """Filter products for a shop category."""
    if not category_slug or category_slug == "all":
        return PRODUCTS
    return [product for product in PRODUCTS if product.category == category_slug]
