from typing import Any

from core import Settings


def apply_theme(chart: Any, settings: Settings) -> Any:
    theme = settings.chart_theme
    palette = theme.palette
    return (
        chart
        .properties(width=theme.width, height=theme.height)
        .configure_view(fill=palette.background, stroke="transparent")
        .configure_axis(
            grid=True,
            gridColor=palette.grid,
            gridOpacity=1.0,
            gridWidth=theme.grid_width,
            domain=False,
            tickColor=theme.axis_color,
            labelFontSize=theme.font_size,
            titleFontSize=theme.font_size + 1,
            labelFont=theme.font_family,
            titleFont=theme.font_family,
            labelColor=theme.label_color,
            titleColor=theme.title_color,
        )
        .configure_legend(
            labelFontSize=theme.font_size,
            titleFontSize=theme.font_size,
            labelFont=theme.font_family,
            titleFont=theme.font_family,
            labelColor=theme.label_color,
            titleColor=theme.title_color,
        )
        .configure_title(
            fontSize=theme.font_size + 3,
            font=theme.font_family,
            color=theme.title_color,
            anchor="start",
        )
        .configure_range(
            category=[
                palette.primary,
                palette.secondary,
                palette.accent,
                palette.success,
                palette.muted,
                palette.highlight,
            ]
        )
    )
