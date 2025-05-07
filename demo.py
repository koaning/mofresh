# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==5.5.0",
#     "anthropic==0.50.0",
#     "anywidget==0.9.18",
#     "marimo",
#     "matplotlib==3.10.1",
#     "mohtml==0.1.7",
#     "numpy==2.2.5",
#     "polars==1.29.0",
#     "pyarrow==18.1.0",
#     "pyobsplot==0.5.3.2",
#     "traitlets==5.14.3",
#     "vl-convert-python==1.7.0",
# ]
# ///

import marimo

__generated_with = "0.13.3"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import io 
    import base64
    import time
    import random
    import anywidget
    import matplotlib 
    import matplotlib.pylab as plt 
    import numpy as np
    import traitlets
    import altair as alt
    import polars as pl
    from tempfile import TemporaryDirectory
    from pathlib import Path

    # This is necessary to prevent matplotlib from causing memory leaks
    # https://stackoverflow.com/questions/31156578/matplotlib-doesnt-release-memory-after-savefig-and-close
    matplotlib.use('Agg')


    def refresh_matplotlib(func):
        def wrapper(*args, **kwargs):
            # Reset the figure to prevent accumulation. Maybe we need a setting for this?
            fig = plt.figure()

            # Run function as normal
            func(*args, **kwargs)

            # Store it as base64 and put it into an image.
            my_stringIObytes = io.BytesIO()
            plt.savefig(my_stringIObytes, format='jpg')
            my_stringIObytes.seek(0)
            my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

            # Close the figure to prevent memory leaks
            plt.close(fig)
            plt.close('all')
            return f'data:image/jpg;base64, {my_base64_jpgData}'
        return wrapper

    @refresh_matplotlib
    def cumsum_linechart(data):
        y = np.cumsum(data)
        plt.plot(np.arange(len(y)), y)
    return (
        Path,
        TemporaryDirectory,
        alt,
        anywidget,
        cumsum_linechart,
        np,
        pl,
        random,
        time,
        traitlets,
    )


@app.cell
def _():
    # from mohtml import img 

    # img(src=cumsum_linechart([1, 2, 3, 2]))
    return


@app.cell
def _(anywidget, traitlets):
    class ImageRefreshWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          let src = () => model.get("src");
          let image = document.createElement("img");
          image.src = src();
          model.on("change:src", () => {
            image.src = src();
          });
          el.appendChild(image);
        }
        export default { render };
        """
        src = traitlets.Unicode().tag(sync=True)
    return (ImageRefreshWidget,)


@app.cell
def _(ImageRefreshWidget, cumsum_linechart, mo):
    widget = mo.ui.anywidget(ImageRefreshWidget(src=cumsum_linechart([1,2,3,4])))
    widget
    return (widget,)


@app.cell
def _(cumsum_linechart, random, time, widget):
    data = [random.random() - 0.5]

    for i in range(20):
        data += [random.random() - 0.5]
        widget.src = cumsum_linechart(data)

        time.sleep(0.2)
    return


@app.cell
def _(Path, TemporaryDirectory, anywidget, traitlets):
    def altair2svg(chart):
        # Need to write to disk to get SVG, filetype determines how to store it
        # have not found an api in altair that can return a variable in memory
        with TemporaryDirectory() as tmp_dir:
            chart.save(Path(tmp_dir) / "example.svg")
            return (Path(tmp_dir) / "example.svg").read_text()

    class SVGRefreshWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
          let elem = () => model.get("svg");
          let div = document.createElement("div");
          div.innerHTML = elem();
          model.on("change:svg", () => {
            div.innerHTML = elem();
          });
          el.appendChild(div);
        }
        export default { render };
        """
        svg = traitlets.Unicode().tag(sync=True)
    return SVGRefreshWidget, altair2svg


@app.cell
def _(altair2svg):
    def refresh_altair(func):
        def wrapper(*args, **kwargs):
            # Run function as normal
            altair_chart = func(*args, **kwargs)
            return altair2svg(altair_chart)
        return wrapper
    return (refresh_altair,)


@app.cell
def _(SVGRefreshWidget, alt, mo, np, pl, refresh_altair):
    @refresh_altair
    def altair_cumsum_chart(data):
        df = pl.DataFrame({
            "x": range(len(data)), "y": np.array(data).cumsum()
        })
        return alt.Chart(df).mark_line().encode(x="x", y="y")

    svg_widget = mo.ui.anywidget(SVGRefreshWidget(svg=altair_cumsum_chart([1, 2])))
    svg_widget
    return altair_cumsum_chart, svg_widget


@app.cell
def _(altair_cumsum_chart, random, svg_widget, time):
    more_data = [random.random() - 0.5 for _ in range(10)]

    for _i in range(10):
        more_data += [random.random() - 0.5]
        svg_widget.svg = altair_cumsum_chart(more_data)
        time.sleep(0.1)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
