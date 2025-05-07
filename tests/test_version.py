import altair as alt
import polars as pl
from mofresh import altair2svg, refresh_altair

def test_version():
    from mofresh import __version__
    assert __version__

def test_altair2svg():
    df = pl.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    chart = alt.Chart(df).mark_point().encode(x="x", y="y")

    @refresh_altair
    def make_chart():
        return chart
    
    assert altair2svg(chart) == make_chart()
