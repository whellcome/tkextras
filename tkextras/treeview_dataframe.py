import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkextras import WidgetsRender


class TreeviewDataFrame(WidgetsRender, ttk.Treeview):
    _svars = {"flag_symbol": {
        "check": "✔",
        "uncheck": " "
    }}
    _svars["flag_values"] = {
        _svars["flag_symbol"]["uncheck"]: _svars["flag_symbol"]["check"],
        _svars["flag_symbol"]["check"]: _svars["flag_symbol"]["uncheck"]
    }
    _svars["check_all"] = {}

    def __init__(self, parent, dataframe=None, render_params=None, *args, **kwargs):
        super().__init__(render_params, parent, *args, **kwargs)
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.bind("<Button-1>", self.toggle_cell)
        if not (dataframe is None):
            self.make_tree(dataframe)

    def make_tree(self, df:pd.DataFrame):
        cols = df.columns.to_list()
        for col in cols:
            self.heading(col, text=col.capitalize())
            if col != "name":
                self.column(col, width=100, anchor="center")
            else:
                self.column(col, width=200, anchor="w")
        for index, row in df.iterrows():
            self.insert("", "end", values=tuple(row))

    @property
    def svars(self):
        return self._svars.copy()

    def column(self, column, option=None, **kw):
        """
            Override column method with DataFrame.
        """
        result = super().column(column, option=option, **kw)
        if column not in self.df.columns:
            self.df[column] = ''
        return result

    def insert(self, parent, index, iid=None, **kw):
        """
               Inserts a new row into the Treeview and synchronizes it with the DataFrame.
               :param parent: Parent node for Treeview (usually "" for root-level items).
               :param index: Position to insert the item.
               :param iid: Unique identifier for the row. If None, Treeview generates one.
               :param kw: Additional arguments for Treeview insert (e.g., values).
               """
        # Use the provided iid or let Treeview generate one
        if iid is None:
            iid = super().insert(parent, index, **kw)  # Automatically generate iid
        else:
            super().insert(parent, index, iid=iid, **kw)

        # Ensure values are provided
        values = kw.get("values", [])

        # Convert values to a DataFrame-compatible dictionary
        new_row = {col: val for col, val in zip(self.cget("columns"), values)}

        # Add the new row to the DataFrame, using iid as the index
        self.df.loc[iid] = new_row
        return iid

    def set(self, item, column=None, value=None):
        """
            Enhanced set method for synchronization with a DataFrame.
            :param item: The item ID (iid) in the Treeview.
            :param column: The column name to retrieve or update.
            :param value: The value to set; if None, retrieves the current value.
            :return: The value as returned by the original Treeview method.
        """
        result = super().set(item, column, value)
        if item not in self.df.index:
            raise KeyError(f"Row with index '{item}' not found in DataFrame.")
        is_filtered = True if item in self.filtered_df.index else False
        if value is None:
            if column is None:
                self.df.loc[item] = self.df.loc[item].replace(result)
            else:
                self.df.loc[item, column] = result
        else:
            self.df.loc[item, column] = value
            if is_filtered:
                self.filtered_df.loc[item, column] = value
            ind = self.cget("columns").index(column) if not column else 0
            self.all_checked_update(ind)
        return result

    def item(self, item, option=None, **kw):
        """
        Override item method with DataFrame.
        """
        values = kw.get("values", [])
        result = super().item(item, option, **kw)
        is_filtered = True if item in self.filtered_df.index else False
        if option is None and len(values):
            updates = pd.Series(values, index=self.cget("columns"))
            self.df.loc[item] = updates
            if is_filtered:
                self.filtered_df.loc[item] = updates
            self.all_checked_update()
        return result

    def delete(self, *items, inplace=False):
        """
        Override delete method with DataFrame..
        """
        if inplace:
            for item in items:
                values = self.item(item, "values")
                self.df = self.df[~(self.df[list(self.df.columns)] == values).all(axis=1)]
        super().delete(*items)

    def flag_inverse(self, value: str) -> str:
        flag_values = self.svars["flag_values"]
        return flag_values[value]

    def toggle_cell(self, event):
        """Handles cell clicks to change flags."""
        if self.identify_region(event.x, event.y) != "cell":
            return
        col_num = int(self.identify_column(event.x).replace("#", "")) - 1
        if not col_num:
            return
        col_name = self.cget("columns")[col_num]
        item = self.identify_row(event.y)
        current_value = self.set(item, col_name)
        self.set(item, col_name, self.flag_inverse(current_value))
        self.event_generate("<<TreeToggleCell>>")

    def rebuild_tree(self, dataframe=None):
        if dataframe is None:
            dataframe = self.df
        self.delete(*self.get_children())
        for index, row in dataframe.iterrows():
            self.insert("", "end", iid=index, values=row.to_list())

    def filter_by_name(self, keyword=""):
        """Filter rows based on a keyword and update Treeview."""
        self.filtered_df = self.df[self.df[self.df.columns[0]].str.contains(keyword, case=False)].copy()
        self.rebuild_tree(self.filtered_df)

    def filter_event_evoke(self):
        """Filter updated event."""
        self.event_generate("<<TreeFilterUpdated>>")

    def all_checked_event_evoke(self):
        self.event_generate("<<TreeCheckAllUpdated>>")

    def is_all_checked(self, column):
        df = self.filtered_df if len(self.filtered_df) else self.df
        return not len(df[df.iloc[:, column] == self.svars["flag_symbol"]["uncheck"]])

    def all_checked_update(self, column=0):
        if not len(self.svars["check_all"]):
            return
        if column:
            self.svars['check_all'][column].set(self.is_all_checked(column))
        else:
            for i in range(1, len(self.cget("columns"))):
                self.svars['check_all'][i].set(self.is_all_checked(i))
        self.all_checked_event_evoke()

    @classmethod
    def transform_df(cls, load_df: pd.DataFrame, names_column: str) -> pd.DataFrame:
        """
        Moves the specified column to the first position in the DataFrame.
        Replace boolean-like values in a DataFrame with custom symbols.
        """

        def replace_boolean_values(df):
            return df.map(
                lambda x: cls._svars["flag_symbol"]["check"] if pd.notna(x) and bool(x) and x not in {" ", "_"}
                else cls._svars["flag_symbol"]["uncheck"])

        if names_column in load_df.columns:
            col_data = load_df.pop(names_column)
            load_df = replace_boolean_values(load_df)
            load_df.insert(0, names_column, col_data)

        return load_df

    def filter_widget(self, parent):
        widget_frame = ttk.Frame(parent, width=150, borderwidth=1, relief="solid", padding=(2, 2))
        self.rgrid(tk.Label(widget_frame, text="Filter by table name:", font=("Helvetica", 9, "bold")),
                   dict(row=0, column=0, pady=5))
        filter_entry = tk.Entry(widget_frame)
        self.rgrid(filter_entry, dict(row=0, column=1, padx=5, pady=5, sticky="ew"))

        def apply_filter():
            self.filter_by_name(filter_entry.get())
            if len(self.filtered_df) == len(self.df):
                self.filtered_df = pd.DataFrame()
            self.filter_event_evoke()
            self.all_checked_update()

        def clear_filter():
            self.rebuild_tree()
            filter_entry.delete(0, tk.END)
            self.filtered_df = pd.DataFrame()
            self.filter_event_evoke()
            self.all_checked_update()

        self.rgrid(ttk.Button(widget_frame, text="Filter", command=apply_filter),
                   dict(row=0, column=2, padx=5, pady=5))
        self.rgrid(ttk.Button(widget_frame, text="Restore", command=clear_filter),
                   dict(row=0, column=3, padx=5, pady=5))
        return widget_frame

    def checkbox_widget(self, parent):

        def toggle_all(index: int):
            checked = self.svars['check_all'][index].get()
            if not checked:
                self.svars['check_all'][index].set(False)
            for item in self.get_children():
                values = list(self.item(item, "values"))
                if checked:
                    values[index] = self.svars['flag_symbol']['check']
                else:
                    values[index] = self.svars['flag_symbol']['uncheck']
                self.item(item, values=values)

        widget_frame = ttk.Frame(parent, padding=(2, 2))

        for i, col in enumerate(self.cget("columns")[1:]):
            ind = i + 1
            self.svars["check_all"][ind] = tk.IntVar(value=0)
            box_text = f"Check all {self.heading(col)['text'] if self.heading(col)['text'] else col}"
            render_params = dict(row=0, column=ind, padx=20)
            self.rgrid(ttk.Checkbutton(widget_frame, text=box_text, variable=self.svars["check_all"][ind],
                                       command=lambda k=ind: toggle_all(k)), render_params)
        return widget_frame
