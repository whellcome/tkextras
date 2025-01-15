import tkinter as tk
from tkinter import ttk

import requests

from tkextras import WidgetsRender


class ExampleFrame(WidgetsRender, ttk.Frame):
    """
        When creating an element, add WidgetsRender to the main parent tk.Widget class
    """

    def __init__(self, *args, **options):

        super().__init__(*args, **options)
        self.create_widgets()

    def create_widgets(self):

        def fetch_quote():
            try:
                response = requests.get("https://api.quotable.io/random")
                quote['text'] = response.json()["content"]
                # The attributes of the rendered element are changed
            except:
                quote['text'] = "This is a quote!"
                # quotable.io is often unavailable, then we get a replacement quote

        grid = self.rgrid
        normal = ("Helvetica", 13)
        italic = ("Helvetica", 11, "italic")

        grid(self)
        grid(tk.Label(self, text="Click the button and get a quote.", font=normal),
             dict(row=0, column=0, columnspan=3, pady=5))
        # there is no need to explicitly create a variable to render an object
        quote = grid(ttk.Label(self, text="", wraplength=250, font=italic), dict(row=1, column=0, columnspan=3))
        # in one command we get a fully rendered object
        grid(tk.Button(self, text=" Fetch Quote! ", command=fetch_quote, font=normal), dict(row=2, column=1, pady=5))


app = ExampleFrame()
app.winfo_toplevel().title("Example WidgetsRender")
app.mainloop()
