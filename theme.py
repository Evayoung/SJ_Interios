"""Brand theme and component defaults for the SJ Interiors website."""

from faststrap import create_theme, set_component_defaults

BRAND_COLORS = {
    "primary": "#6E45C9",
    "secondary": "#D8BC73",
    "accent": "#ECE7F5",
    "white": "#FFFFFF",
    "text": "#2A1D45",
    "muted": "#6C627F",
    "deep": "#1D1234", 
} 

SJ_INTERIORS_THEME = create_theme(
    primary=BRAND_COLORS["primary"],
    secondary=BRAND_COLORS["secondary"],
    success="#8A6FE0",
    info="#B9AED4",
    warning=BRAND_COLORS["secondary"],
    danger="#C8607D",
    light="#F7F4FB",
    dark=BRAND_COLORS["deep"],
)


def setup_sj_interiors_defaults() -> None:
    """Apply shared Faststrap defaults for the website."""
    set_component_defaults("Button", variant="primary", size="md")
    set_component_defaults("Badge", pill=True)
    set_component_defaults("Navbar", variant="light", expand="lg", container=True)
