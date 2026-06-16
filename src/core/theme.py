from pydantic import BaseModel


class ColorPalette(BaseModel):
    model_config = {"frozen": True}

    primary: str = "#1f77b4"
    secondary: str = "#ff7f0e"
    accent: str = "#2ca02c"
    danger: str = "#d62728"
    muted: str = "#7f7f7f"
    highlight: str = "#9467bd"
    background: str = "#f7f7f7"
    grid: str = "#e0e0e0"


class ChartTheme(BaseModel):
    model_config = {"frozen": True}

    width: int = 520
    height: int = 320
    bar_opacity: float = 0.7
    band_opacity: float = 0.3
    line_stroke_width: float = 2.5
    point_size: float = 60.0
    palette: ColorPalette = ColorPalette()
    font_size: int = 13
    font_family: str = "Inter, system-ui, sans-serif"
