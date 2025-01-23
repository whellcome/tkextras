"""
This is a working example of using the TreeviewDataFrame class
"""
import pandas as pd
from tkinter import ttk
from tkextras import WidgetsRender, TreeviewDataFrame
from faker import Faker
fake = Faker()


class ExampleTreeviewDataFrame(WidgetsRender, ttk.Frame):
    """
    Example of TreeviewDataFrame class based on the WidgetsRender and ttk.Frame classes
    """
    def __init__(self, *args, **options):

        super().__init__(*args, **options)
        self.create_widgets()

    def create_widgets(self):
        """
        Placing elements on a form using the rgrid() method

        :return: None
        """
        grid = self.rgrid

        # 1. Prepare a dataframe containing values 0 and 1,
        # values 1 are changed to tree.svars["flag_symbol"]["check"], 0 to tree.svars["flag_symbol"]["uncheck"]:
        url = "https://raw.githubusercontent.com/whellcome/MLGliomaClassification/master/data/TCGA_InfoWithGrade.csv"
        df = pd.read_csv(url).iloc[:99, 4:9]
        df['name'] = df.apply(lambda x: fake.name(), axis=1)  # a fake name to each row
        df = TreeviewDataFrame.transform_df(df, 'name')

        # 2. Creating a TreeviewDataFrame element, and loading the prepared dataframe df during initialization:
        cols = df.columns.to_list()
        tree = TreeviewDataFrame(self, dataframe=df, columns=cols, show="headings")

        grid(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        frame = grid(ttk.Frame(self, padding=(2, 2)), dict(row=0, column=0, columnspan=3, sticky="e"))

        # 3. Render filter and checkbox widgets:
        grid(tree.filter_widget(frame), dict(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew"))
        grid(tree.checkbox_widget(frame), dict(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="e"))

        # 4. Render tree and scrollbar:
        grid(tree, dict(row=1, column=0, pady=5))
        grid(scrollbar, dict(row=1, column=2, sticky="ns"))


app = ExampleTreeviewDataFrame()
app.winfo_toplevel().title("Example TreeviewDataFrame")
app.mainloop()
