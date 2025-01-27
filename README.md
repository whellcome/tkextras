# tkextras

**Enhancing tkinter development with streamlined rendering and DataFrame-powered Treeview.**

tkextras is a lightweight Python library that extends tkinter functionality, making GUI development easier and more
efficient. It introduces a simplified widget rendering system and an extended Treeview component that integrates
seamlessly with pandas DataFrames.

## Features

- **WidgetsRender**: Unified interface for rendering widgets with `grid()`, `pack()`, and `place()` methods.
- **TreeviewDataFrame**: Extended `ttk.Treeview` that synchronizes with `pandas.DataFrame`.
- **Built-in Filtering**: Interactive filtering and flagging for table-based data.
- **Event System Integration**: Custom events for enhanced user interaction.
- **Sphinx Documentation**: Full [API documentation](https://tkextras.readthedocs.io) and usage examples.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/whellcome/tkextras.git
   cd tkextras
   ```

2. Install the module:

```sh
pip install git+https://github.com/whellcome/tkextras.git
```

## Usage

### Rendering Widgets Easily

```python
import tkinter as tk
from tkextras import WidgetsRender


class ExampleApp(WidgetsRender, tk.Tk, ):
  def __init__(self):
    super().__init__()
    lable = self.rgrid(tk.Label(self), dict(row=0, column=0))
    lable['text'] = "Hello, World!"

app = ExampleApp()
app.mainloop()
```
Advanced **[working example](examples/example_widgets_render.py)** of WidgetsRender application


### Working with Treeview and DataFrames

```python
from tkextras import TreeviewDataFrame
import tkinter as tk

root = tk.Tk()
tree = TreeviewDataFrame(root, columns=["Name", "Married", "Employed"], show='headings')
tree.pack(fill="both", expand=True)

tree.insert("", "end", values=("Alice", " ", " "))  # Normal rows addition
tree.insert("", "end", values=("Bob", " ", " "))

tree.make_tree()  # Tree design, can include a Dataframe(transformed, with identical columns) to loading
tree.bind("<<TreeToggleCell>>", lambda x: print(tree.df))  # DataFrame synchronization

root.mainloop()
```
Advanced **[working example](examples/example_treeview_dataframe.py)** of TreeviewDataFrame application:

![Example TreeviewDataFrame](https://raw.githubusercontent.com/whellcome/tkextras/4318f6286a884fd38f3a8827b05bf871910e6a30/example_treeview_dataframe.png)

## Documentation

Complete documentation is available at:

📖 **[Project Documentation](https://tkextras.readthedocs.io)**

## Examples

For real-world applications, see the **examples/** folder, or check out:

- **MS Access to SQL Export Tool** ([GitHub](https://github.com/whellcome/MSAccessToSQL)) - Uses tkextras for UI
  components.

## Contributing

Contributions are welcome! Open an issue or submit a pull request if you have improvements or bug fixes.

> **Need support or have a suggestion?** 🚀🔥  
> Please open an [issue](https://github.com/whellcome/tkextras/issues) on GitHub.

## License

This project is licensed under the MIT License.

---

🚀 **Enhance your tkinter experience with tkextras!**
