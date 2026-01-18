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
        self.entry_cliente = self.input_box(parent, "Cliente", 0, 0)
        self.entry_prod = self.input_box(parent, "Producto", 2, 0)
        self.entry_cant = self.input_box(parent, "Cantidad", 2, 0)
        self.entry_mp = self.input_box(parent, "Materia Prima ($)", 0, 1)
        self.entry_horas = self.input_box(parent, "Horas Prod.", 1, 1)
        self.entry_extras = self.input_box(parent, "Extras ($)", 2, 1)

    def crear_inputs_config(self, parent):
        self.entry_valor_hora = self.input_box(parent, "Valor Hora ($)", 0, 0)
        self.entry_valor_hora.insert(0, "6500")
        self.entry_indirectos.insert(0, "15")
        self.entry_ganancia = self.input_box(parent, "% Ganancia", 0, 1)
        self.entry_ganancia.insert(0, "40")
        self.entry_bonif = self.input_box(parent, "Bonificacion ($)", 1, 1)
        self.entry_bonif.insert(0, "0")

    def input_box(self, parent, placeholder, r, c):
        e = ctk.CTkEntry(parent, placeholder_text=placeholder)
        e.grid(row=r, column=c, padx=10, pady=10, sticky="ew")
        return e

    #EVENTOS

    def evento_calcular(self):
        try:
            #RECOLECCION DE DATOS
            datos = {
                'catidad': self.get_float(self.entry_cant),
                'materia_prima': self.get_float(self.entry_mp),
                'horas': self.get_float(self.entry_horas),
                'extras': self.get_float(self.entry_extras),
                'valor_hora': self.get_float(self.entry_valor_hora),
                'pct_indirectos': self.get_float(self.entry_indirectos),
                'pct_ganancia': self.get_float(self.entry_ganancia),
                'bonificacion': self.get_float(self.entry_bonif)
            }

            #LLAMAMOS A LOGICA
            self.resultados_cache = self.logic.calcular_total(datos)

            #ACTUALIZAMOS UI
            total = self.resultados_cache['total_operacion']
            self.lbl_total.configure(text=f"${total:,.2f}")
            self.btn_pdf.configure(state="normal")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def evento_pdf(self):
        if not self.resultados_cache: return

        datos_form = {
            'cliente': self.entry_cliente.get() or "Consumidor Final", 
            'producto': self.entry_prod.get() or "Varios"
        }

        #LLAMAR A REPORTES
        archivo = self.reporter.generar_presupuesto(datos_form, self.resultados_cache)
        messagebox.showinfo("Exito", f"PDF Generado: {archivo}")

        