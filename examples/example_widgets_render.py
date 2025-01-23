"""
This is a working example of using the WidgetsRender class
"""
import tkinter as tk
from tkinter import ttk
import requests
from tkextras import WidgetsRender


class ExampleFrame(WidgetsRender, ttk.Frame):
    """
        When creating a class, add WidgetsRender to the main parent tk.Widget class
    """

    def __init__(self, *args, **options):

        super().__init__(*args, **options)
        self.create_widgets()

    def create_widgets(self):
        """
        Placing elements on a form using the rgrid() method

        :return: None
        """
        def fetch_quote():
            """
            Fetching a random quote from dummyjson.com
            The attributes of the rendered element are changed dynamically

            :return: None
            """
            try:
                response = requests.get("https://dummyjson.com/quotes/random")
                res = response.json()

                # The attributes of the rendered element are changed dynamically:
                quote['text'] = res["quote"]
                author['text'] = res["author"]

            except ConnectionError:

                # dummyjson.com can be unavailable, then we get a replacement quote:
                quote['text'] = "This is the great quote!"
                author['text'] = "Great Author"

        grid = self.rgrid
        head = ("Helvetica", 13)
        italic = ("Helvetica", 11, "italic")
        underline = ("Helvetica", 11, "underline")

        grid(self)

        # there is no need to explicitly create a variable to render an object:
        grid(tk.Label(self, text="Click the button and get a quote.", font=head), dict(row=0, column=0, columnspan=3))

        # in one command we get a fully rendered object:
        quote = grid(ttk.Label(self, text="", wraplength=250, font=italic), dict(row=1, column=0, columnspan=3))
        author = grid(ttk.Label(self, text="", font=underline), dict(row=2, column=0, columnspan=3, sticky="e"))

        grid(tk.Button(self, text=" Fetch Quote! ", command=fetch_quote, font=head), dict(row=3, column=1))


app = ExampleFrame(dict(pady=5, padx=2))  # setting a parameter common to all elements (x, y offset)
app.winfo_toplevel().title("Example WidgetsRender")
app.mainloop()
