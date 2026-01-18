from fpdf import FPDF
from datetime import datetime

class GeneradorPDF:
    def generar_presupuesto(self, datos_cotizacion, resultados):
        """datos_cotizacion es la info del cliente
        resultados son los calculados en logica.py"""

        cliente = datos_cotizacion['cliente']
        producto = datos_cotizacion['producto']
        fecha = datetime.now().strftime("%d/%m/%Y")

        pdf = FPDF()
        pdf.add_page()

        #HEADER

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO - ANTARES", 0, 1, "C")
        pdf.ln(10)

        #INFO
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Cliente: {cliente}", 0, 1)
        pdf.cell(0, 10, f"Producto: {producto}", 0, 1)
        pdf.cell(0, 10, f"Fecha: {fecha}", 0 , 1)
        pdf.ln(5)

        #TABLA

        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(140, 10, "Concepto", 1, 0, "L", 1)
        pdf.cell(50, 10, "Valor", 1, 1, "R", 1)

        pdf.set_font("Arial", "", 12)

        desglose = resultados['desglose']

        items_a_mostrar = [
            ("Materia Prima", desglose['mp']),
            ("Mano de Obra", desglose['mano_obra']),
            ("Costos Indirectos", desglose['indirectos_valor']),
            ("Extras ", desglose['extras']),
            ("Ganancia Estimada ", desglose['ganancia_valor']),
            ("Bonificacion ", -desglose['bonificacion'])
        ]

        for concepto, valor in items_a_mostrar:
            if valor != 0:
                pdf.cell(140, 10, concepto, 1)
                pdf.cell(50, 10, f"{valor:m 2f}", 1, 1, "R")

            #TOTAL
            pdf.set_font("Arial", "B", 14)
            pdf.cell(140, 10, "TOTAL FINAL", 1, 0, "R")
            pdf.cell(50, 10, f"${resultados['total_operacion']:,.2f}", 1, 1, "R")

            filename = f"Presupuesto_{cliente}_{datetime.now().strftime('%H%M%S')}.pdf"
            pdf.output(filename)
            return filename