class CalculadoraCostos():
    def calcular_total(self, datos):
        """Recibe los inputs crudos y devuelve los resultados calculados"""
        try:
            cant = datos.get('cantidad', 1)
            mp = datos.get('materia_prima', 0)
            horas = datos.get('horas', 0)
            valor_hora = datos.get('valor_hora', 0)
            extras = datos.get('extras', 0)
            pct_indirectos = datos.get('pct_indirectos', 0)
            pct_ganancia = datos.get('pct_ganancia', 0)
            bonif = datos.get('bonificacion', 0)

            #logicas de negocio

            mano_obra = horas * valor_hora
            costo_primo = mp + mano_obra + extras
            costo_indirectos = costo_primo * (pct_indirectos / 100)
            
            costo_total_prod = costo_primo + costo_indirectos

            ganancia_valor = costo_total_prod * (pct_ganancia / 100)
            precio_bruto = costo_total_prod + ganancia_valor
            precio_final = precio_bruto - bonif

            total_operacion = precio_final * cant
            #retornar acomodado

            return {
                "unitario_final:": precio_final,
                "total_operacion": total_operacion,
                "desglose": {
                    "mp": mp,
                    "mano_obra": mano_obra,
                    "extras": extras,
                    "indirectos_valor": costo_indirectos,
                    "ganancia_valor": ganancia_valor,
                    "bonificacion": bonif
                }
            }
        
        except Exception as e:
            raise ValueError(f"Error de calculo: {e}")
        
