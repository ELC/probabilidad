from pydantic import BaseModel


class ColorPalette(BaseModel):
    model_config = {"frozen": True}

    primary: str = "#348ABD"
    secondary: str = "#A60628"
    accent: str = "#7A68A6"
    success: str = "#467821"
    danger: str = "#B22222"
    muted: str = "#CF4457"
    highlight: str = "#188487"
    background: str = "#EEEEEE"
    grid: str = "#FFFFFF"


class ChartTheme(BaseModel):
    model_config = {"frozen": True}

    width: int = 520
    height: int = 320
    bar_opacity: float = 0.85
    band_opacity: float = 0.3
    line_stroke_width: float = 2.5
    point_size: float = 60.0
    palette: ColorPalette = ColorPalette()
    font_size: int = 11
    font_family: str = "DejaVu Sans, sans-serif"
    grid_width: float = 1.5
    label_color: str = "#555555"
    title_color: str = "#222222"
    axis_color: str = "#BCBCBC"
