import math

import pandas as pd


class resultado:
  def __init__(self, capital_total, interes, isr):
    self.capital_total = capital_total
    self.interes = interes
    self.isr = isr
    
def calculo_cetes(capital, plazo):
    capital=float(capital)
    plazo=float(plazo)
    tasa=0.1105
    precio= 10 / (1 + (tasa / 360) * plazo)
    titulos = math.floor(capital/precio)
    remanente=capital%precio
    inversion_cetes=precio*titulos
    interes_bruto = inversion_cetes*(tasa / 360)*plazo
    isr=interes_bruto*0.015
    utilidad_neta= interes_bruto - isr
    capital_total=utilidad_neta+remanente+capital
    capital_total= "${:,.2f}".format(capital_total)
    utilidad_neta= "${:,.2f}".format(utilidad_neta)
    
    res = resultado(capital_total, utilidad_neta, isr)

    # initialize list of lists 
    data = [['Capital Inicial', "${:,.2f}".format(float(capital))],['Plazo', str(plazo) + " días"], ['Interes Neto', res.interes],['Capital Final', res.capital_total]] 
    
    # Create the pandas DataFrame 
    df = pd.DataFrame(data, columns=['Concepto', 'Valor']) 
    return df
    
    return pd
