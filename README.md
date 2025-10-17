<img src="imgs/fresh-green.png" width=125 height=125 align="right" style="z-index: 9999;">


### Mofresh

Widgets, designed for marimo, that can automatically refresh

## Installation

You can install the package using pip:

```bash
uv pip install mofresh
```

## Usage

The goal of this project is to offer a few tools that make it easy for you to refresh charts in marimo. This can be useful during a PyTorch training loop where you might want to update a chart on every iteration, but there are many other use-cases for this too.

### Widgets

The library provides three widgets:

1. **`ImageRefreshWidget`** - Displays images that can be updated dynamically. Perfect for refreshing matplotlib plots or any image content.
2. **`HTMLRefreshWidget`** - Renders HTML content that can be updated on the fly. Great for Altair charts, plotly visualizations, or custom HTML.
3. **`ProgressBar`** - A modern progress bar with dark mode support. Ideal for tracking training loops or long-running operations.

## How it works

The trick to get updating charts to work is to leverage [anywidget](https://anywidget.dev/). These widgets have a loop that is independant of the marimo cells which means that you can update a chart even if the cell hasn't completed running. The goal of this library is to make it easy to use this pattern by giving you a few utilities.

Effectively that means you can expect to see stuff like this in marimo: 

![CleanShot 2025-05-07 at 13 55 42](https://github.com/user-attachments/assets/4ccee74f-b89c-4af5-8188-9124da6d1fa1)

## Live demo 

If you want to dive deep and experience the API, the best way is to explore the live notebook on [Github pages](https://koaning.github.io/mofresh/). 

[Go to live docs.](https://koaning.github.io/mofresh/)
