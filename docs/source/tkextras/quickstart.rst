.. _quickstart:

Quickstart
==========

TkeXtras Framework quick start guide


How to install
--------------

Tested on python 3.9-3.11

.. code::

    pip install git+https://github.com/whellcome/tkextras.git

How to use
----------

- Use **WidgetsRender** to simplify layout management

.. code:: python

    import tkinter as tk
    from tkextras import WidgetsRender


    class ExampleApp(WidgetsRender, tk.Tk, ):
      def __init__(self):
        super().__init__()
        lable = self.rgrid(tk.Label(self), dict(row=0, column=0))
        lable['text'] = "Hello, World!"

    app = ExampleApp()
    app.mainloop()

- Working with **TreeviewDataFrame**, basic example:

.. code:: python

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