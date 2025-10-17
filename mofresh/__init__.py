import importlib.metadata

__version__ = importlib.metadata.version("mofresh") 

import io 
import base64
import anywidget
import matplotlib
import matplotlib.pylab as plt 
import traitlets
from tempfile import TemporaryDirectory
from pathlib import Path


matplotlib.use('Agg')


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


class ProgressBar(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        let getValue = () => model.get("value");
        let getMaxValue = () => model.get("max_value");

        // Check for dark mode via marimo's body class or system preference
        const checkDarkMode = () => {
            return document.body.classList.contains('dark') ||
                   (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
        };

        const container = document.createElement('div');
        container.style.width = '100%';
        container.style.marginBottom = '10px';
        container.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';

        // Label
        const label = document.createElement('div');
        label.style.marginBottom = '8px';
        label.style.fontSize = '13px';
        label.style.fontWeight = '500';

        // Progress bar container
        const barContainer = document.createElement('div');
        barContainer.style.width = '100%';
        barContainer.style.height = '24px';
        barContainer.style.borderRadius = '12px';
        barContainer.style.overflow = 'hidden';

        // Progress fill
        const fill = document.createElement('div');
        fill.style.height = '100%';
        fill.style.transition = 'width 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        fill.style.display = 'flex';
        fill.style.alignItems = 'center';
        fill.style.justifyContent = 'center';

        // Percentage text
        const text = document.createElement('span');
        text.style.fontSize = '11px';
        text.style.fontWeight = '600';
        text.style.color = 'white';
        text.style.textShadow = '0 1px 2px rgba(0,0,0,0.3)';
        text.style.letterSpacing = '0.5px';

        const applyTheme = () => {
            const isDarkMode = checkDarkMode();
            label.style.color = isDarkMode ? '#e0e0e0' : '#333';
            barContainer.style.backgroundColor = isDarkMode ? '#2a2a2a' : '#f0f0f0';
            barContainer.style.border = isDarkMode ? '1px solid #404040' : '1px solid #d0d0d0';
            barContainer.style.boxShadow = isDarkMode ? 'inset 0 1px 3px rgba(0,0,0,0.3)' : 'inset 0 1px 3px rgba(0,0,0,0.1)';
            fill.style.background = isDarkMode
                ? 'linear-gradient(90deg, #5cb85c 0%, #4cae4c 100%)'
                : 'linear-gradient(90deg, #66d966 0%, #4caf50 100%)';
            fill.style.boxShadow = isDarkMode
                ? '0 0 10px rgba(76, 174, 76, 0.3)'
                : '0 0 10px rgba(76, 175, 80, 0.3)';
        };

        const updateDisplay = () => {
            const value = getValue();
            const max = getMaxValue();
            const percentage = max > 0 ? (value / max) * 100 : 0;

            label.textContent = `Progress: ${value} / ${max}`;
            fill.style.width = percentage + '%';
            text.textContent = Math.round(percentage) + '%';

            // Update text visibility based on bar width
            text.style.opacity = percentage > 10 ? '1' : '0';
        };

        fill.appendChild(text);
        barContainer.appendChild(fill);
        container.appendChild(label);
        container.appendChild(barContainer);

        applyTheme();
        updateDisplay();

        model.on('change:value', updateDisplay);
        model.on('change:max_value', updateDisplay);

        // Listen for dark mode changes (both system and marimo)
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
        }

        // Watch for marimo dark mode class changes
        const observer = new MutationObserver(applyTheme);
        observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });

        el.appendChild(container);
    }

    export default { render };
    """

    value = traitlets.Int(0).tag(sync=True)
    max_value = traitlets.Int(100).tag(sync=True)
