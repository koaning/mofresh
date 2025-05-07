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

Effectively that means you can expect to see stuff like this in marimo: 

![CleanShot 2025-05-07 at 13 55 42](https://github.com/user-attachments/assets/4ccee74f-b89c-4af5-8188-9124da6d1fa1)

## Live demo 

If you want to dive deep and experience the API, the best way is to explore the live notebook that hosted on Github pages. 

Go to live docs. 
