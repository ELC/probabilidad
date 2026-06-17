from core.theme import ChartTheme, ColorPalette


def test_color_palette_has_all_colors() -> None:
    palette = ColorPalette()
    for field in ("primary", "secondary", "accent", "danger", "muted", "highlight", "background", "grid"):
        value = getattr(palette, field)
        assert value.startswith("#")
        assert len(value) == 7


def test_color_palette_uses_bmh_blue_as_primary() -> None:
    assert ColorPalette().primary.upper() == "#348ABD"


def test_color_palette_uses_bmh_grey_background() -> None:
    assert ColorPalette().background.upper() == "#EEEEEE"


def test_color_palette_uses_white_grid() -> None:
    assert ColorPalette().grid.upper() == "#FFFFFF"


def test_chart_theme_includes_palette() -> None:
    theme = ChartTheme()
    assert theme.width > 0
    assert theme.height > 0
    assert isinstance(theme.palette, ColorPalette)


def test_chart_theme_has_bmh_styling_fields() -> None:
    theme = ChartTheme()
    assert theme.grid_width > 0
    assert theme.label_color.startswith("#")
    assert theme.title_color.startswith("#")
    assert theme.axis_color.startswith("#")
