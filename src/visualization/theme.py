from typing import Any

from core import Settings


def apply_theme(chart: Any, settings: Settings) -> Any:
    theme = settings.chart_theme
    return (
        chart
        .properties(width=theme.width, height=theme.height)
        .configure_axis(
            grid=True,
            gridColor=theme.palette.grid,
            labelFontSize=theme.font_size,
            titleFontSize=theme.font_size,
            labelFont=theme.font_family,
            titleFont=theme.font_family,
        )
        .configure_view(stroke="transparent")
        .configure_legend(labelFontSize=theme.font_size, titleFontSize=theme.font_size)
        .configure_title(fontSize=theme.font_size + 2, font=theme.font_family)
    )
