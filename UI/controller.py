import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.current_year = None
        self.current_shape = None


    def handle_graph(self, e):
        self._view.txt_result1.clean()
        anno = self._view.ddyear.value
        forma = self._view.ddshape.value
        if anno is None or forma is None:
            self._view.create_alert("Selezionare un anno e una forma")
        self._model.build_graph(anno, forma)
        self._view.txt_result1.controls.append(ft.Text(f"Grafo creato con numero di vertici: {self._model.get_num_nodes()}"))
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di archi: {self._model.get_num_edges()}"))
        self._view.update_page()
        archi = self._model.get_archi_peso_maggiore()
        for arco in archi:
            self._view.txt_result1.controls.append(ft.Text(f"id1: {arco[0].id} -> id2: {arco[1].id} - peso: {arco[2]["weight"]}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDYear(self):
        anni = self._model.get_year()
        self._view.ddyear.options.clear()
        for a in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(f"{a}"))
        self._view.update_page()

    def fillDDShape(self, e):
        self._view.ddshape.options.clear()
        anno = self._view.ddyear.value
        forme = self._model.get_shapes(anno)
        for forma in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(text = forma,
                                                                 data = forma))
        self._view.update_page()