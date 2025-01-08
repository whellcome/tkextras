### Documentation and Setup for `tkextras`

Below is the documentation and setup for the `tkextras` module. It contains two classes, `WidgetsRender` and `TreeviewDataFrame`, designed to simplify the rendering of Tkinter elements and enhance `ttk.Treeview` functionality by integrating it with a `pandas.DataFrame`.

---

## File Structure
```
tkextras/
│
├── __init__.py
├── widgets_render.py
└── treeview_dataframe.py
```

### `widgets_render.py`
This file contains the `WidgetsRender` class, which provides methods (`rgrid`, `rpack`, `rplace`) for rendering Tkinter widgets with reusable parameter sets.

#### Example Usage:
```python
import tkinter as tk
from tkextras import WidgetsRender

class ExampleApp(WidgetsRender, tk.Tk,):
    def __init__(self):
        super().__init__()
        self.rgrid(tk.Label(self, text="Hello, World!"), dict(row=0, column=0))

app = ExampleApp()
app.mainloop()
```

---

### `treeview_dataframe.py`
This file contains the `TreeviewDataFrame` class, which extends `ttk.Treeview` and integrates it with `pandas.DataFrame`, offering advanced features like filtering, synchronization, and custom widgets.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tkextras.git
   cd tkextras
   ```

2. Install the module:
   ```bash
   pip install git+https://github.com/whellcome/tkextras.git
   ```

---

## Features
- **Reusable Rendering Methods**: Simplify widget placement with `rgrid`, `rpack`, and `rplace`.
- **Treeview Integration with pandas**: Synchronize and filter data between `ttk.Treeview` and `pandas.DataFrame`.
- **Treeview Custom Widgets**: Add filtering and checkbox widgets for enhanced interactivity.
