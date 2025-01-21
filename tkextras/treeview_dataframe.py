"""
Contains the implementation of the class TreeviewDataFrame
"""
import tkinter as tk
from tkinter import ttk
from typing import Any, Literal

import pandas as pd
from tkextras import WidgetsRender


class TreeviewDataFrame(WidgetsRender, ttk.Treeview):
    """
    Special tree implementation for working with boolean marks (by default {"check": "✔", "uncheck": " "}).
    Supports optional Filtering and "mark all" widgets.
    Simple loading and unloading of a dataframe containing the current state of the tree for further work.
    """
    _svars = {
        "flag_symbol": {
            "check": "✔",
            "uncheck": " "
        },
        "check_all": {}
    }
    _svars["flag_values"] = {
        _svars["flag_symbol"]["uncheck"]: _svars["flag_symbol"]["check"],
        _svars["flag_symbol"]["check"]: _svars["flag_symbol"]["uncheck"]
    }

    def __init__(self, parent: tk.Widget, dataframe: pd.DataFrame = None, render_params: dict = None, *args, **kwargs):
        """

        :param parent:
        :param dataframe:
        :param render_params:
        :param args:
        :param kwargs:
        """
        super().__init__(render_params, parent, *args, **kwargs)
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.bind("<Button-1>", self.toggle_cell)
        if not (dataframe is None):
            self.make_tree(dataframe)

    def make_tree(self, df: pd.DataFrame):
        """

        :param df:
        :return:
        """
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
        """
        The attribute that automatically creates a copy _svars, so that each object has an isolated copy
        :return: dict, isolated svars
        """
        return self._svars.copy()

    def column(self, column: str | int, option=None, **kw):
        """
            Override column method with DataFrame.
        """
        result = super().column(column, option=option, **kw)
        if column not in self.df.columns:
            self.df[column] = ''
        return result

    def insert(self, parent: str, index: int | Literal["end"], iid: str | int | None = None, **kw):
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

    def set(self, item: str | int, column: None = None, value: None = None) -> dict[str, Any]:
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

    def item(self, item: str | int, option: Literal["text"] | None = None, **kw) -> str:
        """
        Override item method with DataFrame synchronization.
        :param item:
        :param option:
        :param kw:
        :return:
        """
        values = kw.get("values", [])
        result = super().item(item, option, **kw)  # noqa
        is_filtered = True if item in self.filtered_df.index else False
        if option is None and len(values):
            updates = pd.Series(values, index=self.cget("columns"))
            self.df.loc[item] = updates
            if is_filtered:
                self.filtered_df.loc[item] = updates
            self.all_checked_update()
        return result

    def delete(self, *items: str | int, inplace=False):
        """
        Override delete method with DataFrame synchronization.
        :param items:
        :param inplace:
        :return:
        """
        if inplace:
            for item in items:
                values = self.item(item, "values")  # noqa
                self.df = self.df[~(self.df[list(self.df.columns)] == values).all(axis=1)]
        super().delete(*items)

    def flag_inverse(self, value: str) -> str:
        """

        :param value: incoming flag
        :return: inverted flag
        """
        flag_values = self.svars["flag_values"]
        return flag_values[value]

    def toggle_cell(self, event):
        """
        Handles cell clicks to change flags.
        :param event: click coordinates
        :return: None if the click is outside the target area
        """
        if self.identify_region(event.x, event.y) != "cell":
            return
        col_num = int(self.identify_column(event.x).replace("#", "")) - 1
        if not col_num:
            return
        col_name = self.cget("columns")[col_num]
        item = self.identify_row(event.y)
        current_value = self.set(item, col_name)
        self.set(item, col_name, self.flag_inverse(current_value))  # noqa
        self.event_generate("<<TreeToggleCell>>")

    def rebuild_tree(self, dataframe: pd.DataFrame = None):
        """

        :param dataframe:
        :return: None
        """
        if dataframe is None:
            dataframe = self.df
        self.delete(*self.get_children())
        for index, row in dataframe.iterrows():
            self.insert("", "end", iid=str(index), values=row.to_list())

    def filter_by_name(self, keyword: str = ""):
        """
        Filter DataFrame rows based on a keyword and update Treeview.
        :param keyword: filter string
        :return: None
        """
        self.filtered_df = self.df[self.df[self.df.columns[0]].str.contains(keyword, case=False)].copy()
        self.rebuild_tree(self.filtered_df)

    def filter_event_evoke(self):
        """
        Filter updated event.
        :return: None
        """
        self.event_generate("<<TreeFilterUpdated>>")

    def all_checked_event_evoke(self):
        """
        Generation of an all_checked flag updated event
        :return:
        """
        self.event_generate("<<TreeCheckAllUpdated>>")

    def is_all_checked(self, column: int) -> bool:
        """
        Checking the column status (all cells are marked)
        :param column: column number
        :return: column status
        """
        df = self.filtered_df if len(self.filtered_df) else self.df
        return not len(df[df.iloc[:, column] == self.svars["flag_symbol"]["uncheck"]])

    def all_checked_update(self, column: int = 0):
        """
        Update the state of all (or one) flags, if column is not 0.
        :param column: column number
        :return: None
        """
        if not len(self.svars["check_all"]):
            return
        if column:
            self.svars['check_all'][column].set(self.is_all_checked(column))  # noqa
        else:
            for i in range(1, len(self.cget("columns"))):
                self.svars['check_all'][i].set(self.is_all_checked(i))  # noqa
        self.all_checked_event_evoke()

    @classmethod
    def transform_df(cls, load_df: pd.DataFrame, names_column: str) -> pd.DataFrame:
        """
        Moves the specified column to the first position in the DataFrame.
        Replace boolean-like values in a DataFrame with custom symbols.
        :param load_df:
        :param names_column:
        :return:
        """

        def replace_boolean_values(df: pd.DataFrame):
            """
            Replace boolean-like values in a DataFrame with custom symbols
            :param df:
            :return:
            """
            return df.map(
                lambda x: cls._svars["flag_symbol"]["check"] if pd.notna(x) and bool(x) and x not in {" ", "_"}
                else cls._svars["flag_symbol"]["uncheck"])

        if names_column in load_df.columns:
            col_data = load_df.pop(names_column)
            load_df = replace_boolean_values(load_df)
            load_df.insert(0, names_column, col_data)

        return load_df

    def filter_widget(self, parent: tk.Widget) -> ttk.Frame:
        """
        Tree filtering widget by word or part of it
        "Filter" button Applies a filter
        "Restore" = clearing the filter value, returning the tree to its original state
        :param parent: specify the parent widget
        :return: ttk.Frame element ready to rendering
        """
        widget_frame = ttk.Frame(parent, width=150, borderwidth=1, relief="solid", padding=(2, 2))
        self.rgrid(tk.Label(widget_frame, text="Filter by table name:", font=("Helvetica", 9, "bold")),
                   dict(row=0, column=0, pady=5))
        filter_entry = tk.Entry(widget_frame)
        self.rgrid(filter_entry, dict(row=0, column=1, padx=5, pady=5, sticky="ew"))

        def apply_filter():
            """
            Applying a filter
            """
            self.filter_by_name(filter_entry.get())
            if len(self.filtered_df) == len(self.df):
                self.filtered_df = pd.DataFrame()
            self.filter_event_evoke()
            self.all_checked_update()

        def clear_filter():
            """
            Clearing the filter value, returning the tree to its original state
            :return:  None
            """
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

    def checkbox_widget(self, parent: tk.Widget) -> ttk.Frame:
        """
        The widget returns "check all" checkboxes for each column, starting with the second one.
        Interactive response to the use of a filter and clicking on cells
        :param parent: specify the parent widget
        :return: ttk.Frame element ready to rendering
        """
        def toggle_all(index: int):
            """
            Invert the value of the mark in the column specified by index
            :param index: column index
            :return: None
            """
            checked = self.svars['check_all'][index].get()  # noqa
            if not checked:
                self.svars['check_all'][index].set(False)  # noqa
            for row in self.get_children():
                values = list(self.item(row, "values"))  # noqa
                if checked:
                    values[index] = self.svars['flag_symbol']['check']
                else:
                    values[index] = self.svars['flag_symbol']['uncheck']
                self.item(row, values=values)

        widget_frame = ttk.Frame(parent, padding=(2, 2))

        for i, col in enumerate(self.cget("columns")[1:]):
            ind = i + 1
            self.svars["check_all"][ind] = tk.IntVar(value=0)  # noqa
            box_text = f"Check all {self.heading(col)['text'] if self.heading(col)['text'] else col}"
            render_params = dict(row=0, column=ind, padx=20)
            self.rgrid(ttk.Checkbutton(widget_frame, text=box_text, variable=self.svars["check_all"][ind],  # noqa
                                       command=lambda k=ind: toggle_all(k)), render_params)
        return widget_frame
