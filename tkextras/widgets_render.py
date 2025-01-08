import tkinter as tk


class WidgetsRender:
    def __init__(self, render_params=None, *args, **options):
        """
        Initialization of the Frame, description of the main elements
        :param render_params: General parameters for the arrangement of elements can be set externally
        :param args:
        :param options:
        """
        super().__init__(*args, **options)
        if render_params is None:
            render_params = dict(sticky="ew", padx=5, pady=2)
        self.__render_params = render_params

    def param_prepare(self, pack_params, func="grid"):
        pack_params = pack_params if pack_params else {}
        united_pack_params = self.__render_params.copy()
        if func == "pack":
            if "sticky" in united_pack_params:
                united_pack_params["anchor"] = united_pack_params.pop("sticky")
        elif func == "place":
            if "sticky" in united_pack_params:
                united_pack_params["anchor"] = united_pack_params.pop("sticky")
        united_pack_params.update(pack_params)
        return united_pack_params

    def rgrid(self, obj: tk.Widget, render_params=None):
        """
        Perform element creation and rendering in one command. Without creating a variable unnecessarily.
        Combines general parameters for the arrangement of elements and parameters for a specific element.
        :param obj: Element to rendering
        :param pack_params: Dictionary with element parameters
        :return: Rendered element
        """
        if obj:
            obj.grid(self.param_prepare(render_params,"grid"))
        return obj

    def rpack(self, obj: tk.Widget, render_params=None):
        if obj:
            obj.pack(self.param_prepare(render_params, "pack"))
        return obj

    def rplace(self, obj: tk.Widget, render_params=None):
        if obj:
            obj.place(self.param_prepare(render_params, "place"))
        return obj

