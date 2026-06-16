from core.theme import ChartTheme, ColorPalette


def test_color_palette_has_all_colors() -> None:
    palette = ColorPalette()
    for field in ("primary", "secondary", "accent", "danger", "muted", "highlight", "background", "grid"):
        value = getattr(palette, field)
        assert value.startswith("#")
        assert len(value) == 7


def test_chart_theme_includes_palette() -> None:
    theme = ChartTheme()
    assert theme.width > 0
    assert theme.height > 0
    assert isinstance(theme.palette, ColorPalette)
