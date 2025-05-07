# Mofresh

A Python package for fresh data processing.

## Installation

You can install the package using pip:

```bash
uv pip install mofresh
```

## Usage

The goal of this project is to offer a few tools that make it easy for you to refresh charts in marimo. This can be useful during a PyTorch training loop where you might want to update a chart on every iteration, but there are many other use-cases for this too.

## How it works

The trick to get updating charts to work is to leverage [anywidget](https://anywidget.dev/). These widgets have a loop that is independant of the marimo cells which means that you can update a chart even if the cell hasn't completed running. The goal of this library is to make it easy to use this pattern by giving you a few utilities.

### Example with `matplotlib`

The easiest way to update matplotlib charts is to first write a function that can generate a chart. The most common way to use matplotlib is to use syntax like `plt.plot(...)` followed by a `plt.show(...)` and the best way to capture all of these layers is to wrap them all ina single function. Once you have such a function, you can use the `@refresh_matplotlib` decorator to turn this function into something that we can use in a refreshable-chart.

```python {.marimo}
import matplotlib.pylab as plt
from mofresh import refresh_matplotlib

@refresh_matplotlib
def cumsum_linechart(data):
    y = np.cumsum(data)
    plt.plot(np.arange(len(y)), y)
```

The decorator takes the matplotlib image and turns it into a base64 encoded string that can be plotted by `<img>` tags in html. You can see this for yourself in the example below. The `img(src=...)` function call in `mohtml` is effectively a bit of syntactic sugar around `<img src="...">`.

```python {.marimo}
from mohtml import img 

img(src=cumsum_linechart([1, 2, 3, 2]))
```

Having a static image is great, but we want dynamic images! That's where our `ImageRefreshWidget` comes in.

```python {.marimo}
from mofresh import ImageRefreshWidget

widget = mo.ui.anywidget(ImageRefreshWidget(src=cumsum_linechart([1,2,3,4])))
widget
```

When you re-run the cell below you should see that the widget updates. This works because the widget knows how to respond to a change to the `widget.src` property. You only need to make sure that you pass along a base64 string that html images can handle, which is covered by the decorator that we applied earlier.

```python {.marimo}
import random 
import time 

data = [random.random() - 0.5]

for i in range(20):
    data += [random.random() - 0.5]
    # This one line over here causes the update!
    widget.src = cumsum_linechart(data)
    time.sleep(0.2)
```