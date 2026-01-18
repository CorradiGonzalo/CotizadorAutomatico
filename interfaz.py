import customtkinter as ctk
from tkinter import messagebox
#IMPORT DE MODULOS 
from logica import CalculadoraCostos
from reportes import GeneradorPDF

ctk.set_appearence_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class AntaresApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logic = CalculadoraCostos()
        self.reporter = GeneradorPDF()
        self.resultados_cache = None
        self.setup_ui()

    def setup_ui(self):
        self.title("Antares | Cotizador Modular v2.0")
        self.geometry("800x650")
        self.resizable(False, False)

        #HEADER
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(full="x", padx=20, pady=10)
        ctk.CTkLabel(header, text="ANTARES QUOTER", font=("Roboto", 24, "bold")).pack(side="left")

        #TABS
        self.tab_view = ctk.CTkTabView(self, width=760, height=400)
        self.tab_cotiz = self.tab_view.add("Datos")
        self.tab_config = self.tab_view.add("Configuracion")

        #UI TAB DATOS
        self.crear_inputs_datos(self.tab_cotiz)
        #UI TAB CONFIG
        self.crear_inputs_config(self.tab_config)

        #FOOTER
        self.footer.pack(fill="x", side="bottom")

        self.btn_calc = ctk.CTkButton(self.footer, text="CALCULAR", font=("Roboto", 16, "bold"), height=50, width=150, fg_color="#0066cc", command=self.evento_calcular)
        self.btn_calc.pack(side="left", padx=40, pady=20)
        self.lbl_total = ctk.CTkLabel(self.footer, text="$0.00", font=("Roboto", 30, "bold"), text_color="#00ff88")
        self.lbl_total.pack(side="right", padx=40)
        self.btn_pdf = ctk.CTkButton(self.footer, text="PDF", state="disabled", widht=100, command=self.evento_pdf)
        self.btn_pdf.pack(side="right", padx=10)

    def crear_inputs_datos(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
