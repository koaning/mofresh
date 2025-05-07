import importlib.metadata

__version__ = importlib.metadata.version("mofresh") 

import io 
import base64
import anywidget
import matplotlib.pylab as plt 
import traitlets
from tempfile import TemporaryDirectory
from pathlib import Path


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


def altair2svg(chart):
    # Need to write to disk to get SVG, filetype determines how to store it
    # have not found an api in altair that can return a variable in memory
    with TemporaryDirectory() as tmp_dir:
        chart.save(Path(tmp_dir) / "example.svg")
        return (Path(tmp_dir) / "example.svg").read_text()


class HTMLRefreshWidget(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
      let elem = () => model.get("html");
      let div = document.createElement("div");
      div.innerHTML = elem();
      model.on("change:html", () => {
        div.innerHTML = elem();
      });
      el.appendChild(div);
    }
    export default { render };
    """
    html = traitlets.Unicode().tag(sync=True)


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


def refresh_altair(func):
    def wrapper(*args, **kwargs):
        # Run function as normal
        altair_chart = func(*args, **kwargs)
        return altair2svg(altair_chart)
    return wrapper
