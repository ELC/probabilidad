from visualization import VennTwoSetsInput, chart_venn_two_sets
from core import Settings

fig = chart_venn_two_sets(
    VennTwoSetsInput(
        probability_a=0.5,
        probability_b=0.4,
        probability_intersection=0.2,
        settings=Settings(),
    )
)
print("Has _repr_png_:", hasattr(fig, "_repr_png_"))
print("Has _repr_html_:", hasattr(fig, "_repr_html_"))
png = fig._repr_png_() if hasattr(fig, "_repr_png_") else None
print("_repr_png_ result:", "bytes len=" + str(len(png)) if png else repr(png))
html = fig._repr_html_() if hasattr(fig, "_repr_html_") else None
print("_repr_html_ result:", repr(html)[:80] if html else repr(html))
