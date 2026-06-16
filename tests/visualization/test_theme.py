import altair as alt

from core import Settings
from visualization import apply_theme


def test_apply_theme_returns_themed_chart() -> None:
    chart = alt.Chart().mark_line()
    themed = apply_theme(chart, Settings())
    assert themed is not None
