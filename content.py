"""Content and sample data for the SJ Interiors website."""

from __future__ import annotations

import os
from dataclasses import dataclass

BUSINESS_NAME = "SJ Interiors"
BUSINESS_SUBTITLE = "Deco and Beddings"
TAGLINE = "Redefining your space with simplicity, comfort, and style."
SHORT_INTRO = (
    "SJ Interiors curates curtains, window blinds, bedsheets, duvets, pillows, and soft decor "
    "essentials that make homes feel calm, stylish, and beautifully put together."
)

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "2348026022672")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "+234 (911) 507-6282")
PHONE_NUMBERS = os.getenv("PHONE_NUMBERS", "08026022672,09115076282").split(",")
ADDRESS = os.getenv(
    "ADDRESS",
    "Limca Junction Shopping Complex, Along Asa Dam Road, Ilorin, Kwara State",
)
LOCATION_SHORT = os.getenv("LOCATION_SHORT", "Ilorin, Kwara State")


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

@dataclass(frozen=True)
class ServiceCategory:
    id: str
    number: int
    title: str
    summary: str
    icon: str
    image: str
    items: list[dict[str, str]]


SERVICE_CATEGORIES = [
    ServiceCategory(
        id="sitting_curtains",
        number=1,
        title="Sitting Room Curtains & Window Dressing",
        summary="Custom drapery tailored for high aesthetic appeal, light control, and room elegance.",
        icon="layout-sidebar-inset",
        image="https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "Luxury Curtain Fabric Dressing", "desc": "Custom yardage tailored to room height"},
            {"name": "Curtain Pleating Tape & Header Styling", "desc": "Precision French, pinch or box pleating"},
            {"name": "Inner Sheer Lining Fabric", "desc": "Daylight-filtering soft sheer drapes"},
            {"name": "Heavy Duty Bronze / Metal Rods", "desc": "Sturdy double/single curtain poles"},
            {"name": "Finials, Brackets & Wall Hardware", "desc": "Reinforced architectural wall mounts"},
            {"name": "Decorative Tie Backs & Holdbacks", "desc": "Matching holdback tassels or metal hooks"},
            {"name": "Custom Tailoring & Finishing Workmanship", "desc": "Master artisan stitching & hems"},
        ],
    ),
    ServiceCategory(
        id="bedroom_curtains",
        number=2,
        title="Bedroom Curtains & Light Control",
        summary="Pleated blackout drapes and sheer linings designed for restful sleep and privacy.",
        icon="moon",
        image="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "Bedroom Curtain Fabrics", "desc": "Blackout, dim-out and velvet drapery"},
            {"name": "Eyelet / Pole Rings & Pleat Tape", "desc": "Smooth gliding hardware fittings"},
            {"name": "Inner Lining Sheers", "desc": "Privacy sheers for soft daylight illumination"},
            {"name": "Bedroom Curtain Rods & Poles", "desc": "Matte black or bronze pole sets"},
            {"name": "Curtain Tie Backs", "desc": "Fabric holdbacks matching bedding tones"},
            {"name": "Custom Bedroom Sewing Workmanship", "desc": "Neat seam-matched tailoring"},
        ],
    ),
    ServiceCategory(
        id="interior_decor_blinds",
        number=3,
        title="Interior Decor, Window Blinds & Lighting",
        summary="Modern window blinds, wall framing, chandeliers, mirrors, and indoor plants.",
        icon="gem",
        image="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "Custom Window Blinds (Roller, Zebra, Venetian)", "desc": "Kitchen, bathroom & office window fittings"},
            {"name": "Decorative Wall Art Framing Sets", "desc": "Gallery-grade framed wall accents"},
            {"name": "Chandeliers & Statement Lighting", "desc": "Living room & dining ambient fixtures"},
            {"name": "Indoor Potted Decorative Plants", "desc": "Lifelike botanical greenery & planters"},
            {"name": "Decorative Wall Accent Mirrors", "desc": "Light-expanding gold and wooden mirrors"},
            {"name": "Welcome Doormats & Room Accent Rugs", "desc": "Anti-slip plush entrance and bedside mats"},
        ],
    ),
    ServiceCategory(
        id="bedroom_bedding",
        number=4,
        title="Bedroom & Luxury Bedding Furnishing",
        summary="High-density mattresses, 400-thread count bedsheets, luxury duvets, and pillows.",
        icon="stars",
        image="https://images.unsplash.com/photo-1464890100898-a385f744067f?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "High-Density Mattresses (6x6 King / 4x6 Double)", "desc": "Orthopedic & luxury support mattress cores"},
            {"name": "Cotton Bedsheet Bundles (6x6 & 4x6)", "desc": "Crisp hotel sheets with matching pillowcases"},
            {"name": "Luxury White Duvet Sets", "desc": "400TC boutique-grade down alternative duvets"},
            {"name": "Patterned & Textured Duvet Sets", "desc": "Designer jacquard and geometric duvet wraps"},
            {"name": "Standard Comfort Fiber Pillows", "desc": "High-resilience soft fiber sleeping pillows"},
        ],
    ),
    ServiceCategory(
        id="kitchenware_utensils",
        number=5,
        title="Kitchenware & Turnkey Apartment Utensils",
        summary="Complete kitchen setups for luxury homes, shortlet apartments, and hospitality suites.",
        icon="cup-hot",
        image="https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "Premium Non-Stick Cookware Pot Sets", "desc": "Multi-piece granite & Teflon non-stick pans"},
            {"name": "Kitchen Burner Stoves & Appliances", "desc": "Gas & electric countertop burner units"},
            {"name": "Complete Cutlery Spoon & Fork Sets", "desc": "Stainless steel mirror-finish cutlery"},
            {"name": "Complete Dinnerware Plate Sets & Glassware", "desc": "Ceramic plate sets, wine & water glasses"},
            {"name": "Chef Knife Sets & Kitchen Utensils", "desc": "Food prep knives, spatulas & ladles"},
            {"name": "Water Dispensers & Water Heaters", "desc": "Appliance installation & setup"},
            {"name": "Dish Drying Racks, Waste Bins & Floor Mats", "desc": "Kitchen organization and safety fittings"},
        ],
    ),
    ServiceCategory(
        id="logistics_workmanship",
        number=6,
        title="Logistics, Measurement & Installation Labor",
        summary="On-site window measurement verification, nationwide delivery, and master installation.",
        icon="tools",
        image="https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=1200&q=80",
        items=[
            {"name": "On-Site Window & Room Measurement", "desc": "Precision laser and tape dimension audit"},
            {"name": "Transportation & Nationwide Logistics", "desc": "Secure transit across Kwara & Nigeria"},
            {"name": "Professional Assembly, Fitting & Mounting", "desc": "Dust-free wall drilling and drapery hanging"},
        ],
    ),
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


TESTIMONIALS = [
    {
        "name": "Dr. Halima Ibrahim",
        "location": "GRA, Ilorin",
        "role": "Homeowner",
        "rating": 5,
        "review": "SJ Interiors transformed our 4-bedroom duplex with custom pleated blackout curtains and hotel-white bedding bundles. The quality and neat finishing exceeded our expectations!",
        "item": "Blackout Curtains & Hotel Bedding",
    },
    {
        "name": "Tunde Bakare",
        "location": "Tanke, Ilorin",
        "role": "Shortlet Apartment Host",
        "rating": 5,
        "review": "I order all bedsheets, duvets, and window blinds for my Airbnb apartments from SJ Interiors. Guests constantly compliment the comfort and crisp luxury feel.",
        "item": "Wholesale Bedsheet & Duvet Supply",
    },
    {
        "name": "Amina Olatunji",
        "location": "Fate Road, Ilorin",
        "role": "Interior Styling Client",
        "rating": 5,
        "review": "Super responsive on WhatsApp! They helped me pick the right curtain fabrics and throw pillow combinations to match my living room sofa. 10/10 recommend.",
        "item": "Curtains & Velvet Throw Pillows",
    },
]

TRANSFORMATIONS = [
    {
        "title": "Living Room Window Elevation",
        "category": "Curtains & Blinds",
        "before_desc": "Bare window with harsh afternoon glare and no softness.",
        "after_desc": "Layered soft sheer drapes with pleated blackout curtains that soften sunlight and create warmth.",
        "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?auto=format&fit=crop&w=1200&q=80",
        "tag": "Window Styling",
    },
    {
        "title": "Hotel-Grade Master Bed Dressing",
        "category": "Bedding & Linen",
        "before_desc": "Plain mattress with unmatched sheets and flat pillows.",
        "after_desc": "Crisp 400-thread count duvet, plush pillow trio, and textured throw accents for a boutique suite aesthetic.",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=80",
        "tag": "Bedding Makeover",
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

