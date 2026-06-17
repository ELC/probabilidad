import altair as alt

from core import Settings
from visualization import apply_theme


def test_apply_theme_returns_themed_chart() -> None:
    chart = alt.Chart().mark_line()
    themed = apply_theme(chart, Settings())
    assert themed is not None


def test_apply_theme_uses_bmh_background_in_serialized_spec() -> None:
    chart = alt.Chart().mark_line()
    spec = apply_theme(chart, Settings()).to_dict()
    config = spec["config"]
    assert config["view"]["fill"].upper() == "#EEEEEE"


def test_apply_theme_uses_bmh_white_gridlines() -> None:
    chart = alt.Chart().mark_line()
    spec = apply_theme(chart, Settings()).to_dict()
    config = spec["config"]
    assert config["axis"]["gridColor"].upper() == "#FFFFFF"
    assert config["axis"]["domain"] is False


def test_apply_theme_assigns_bmh_category_palette() -> None:
    chart = alt.Chart().mark_line()
    spec = apply_theme(chart, Settings()).to_dict()
    category = spec["config"]["range"]["category"]
    assert "#348ABD" in [color.upper() for color in category]
    assert "#A60628" in [color.upper() for color in category]
