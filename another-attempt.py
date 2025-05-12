import marimo

__generated_with = "0.13.6"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import time
    return mo, time


@app.cell
def _(mo, time):
    for i in range(10):
        time.sleep(0.2)
        mo.output.replace(i)
    return


@app.cell
def _():
    import altair as alt
    import polars as pl
    import numpy as np
    import random
    return alt, np, pl, random


@app.cell
def _(alt, mo, np, pl, random):
    data = []
    for j in range(1000): 
        data.append(random.random() - 0.5)
        df = pl.DataFrame({"x": range(len(data)), "y": np.cumsum(data)})
        mo.output.replace(alt.Chart(df).mark_line().encode(x="x", y="y"))
    return


@app.cell
def _(mo):
    mo.md(r"""This approach does kind of work ... but what about matplotlib? What about combining views together? We probably want to decouple the "loop" and the "view". """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
