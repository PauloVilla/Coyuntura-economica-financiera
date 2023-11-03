import datetime as dt
import math

import numpy as np
import pandas as pd

from cetes import Cetes


class resultado:
    def __init__(self, capital_total, interes, isr, periodos):
        self.capital_total = capital_total
        self.interes = interes
        self.isr = isr
        self.periodos = periodos


def calculo_cetes(capital_inicial, plazo, años):
    cetes = Cetes(str(int(plazo)))
    start_date = '2010-01-01'
    end_date = str(dt.date.today())
    tasas = cetes.get_data(date_end=end_date, date_start=start_date)
    tasas = tasas['value']
    periodos = int(años)*364/int(plazo)
    periodos = math.floor(periodos)
    capital_total = capital_inicial
    interes_neto_total = 0
    años_transurridos = 0
    tasa = 0.1105

    for i in range(periodos):

        if i > 0:
            if plazo == 28:
                if i % 13 == 0:
                    años_transurridos = años_transurridos+1
                    tasas = np.append(tasas, np.mean(tasas))
                    tasas = np.delete(tasas, 0)
            if plazo == 91:
                if i % 4 == 0:
                    años_transurridos = años_transurridos+1
                    tasas = np.append(tasas, np.mean(tasas))
                    tasas = np.delete(tasas, 0)
            if plazo == 182:
                if i % 2 == 0:
                    años_transurridos = años_transurridos+1
                    tasas = np.append(tasas, np.mean(tasas))
                    tasas = np.delete(tasas, 0)
            if plazo == 364:
                años_transurridos = años_transurridos+1
                tasas = np.append(tasas, np.mean(tasas))
                tasas = np.delete(tasas, 0)

        tasa = np.mean(tasas)
        capital = float(capital_total)
        plazo = float(plazo)
        precio = 10 / (1 + (tasa / 364) * plazo)
        titulos = math.floor(capital/precio)
        remanente = capital % precio
        inversion_cetes = precio*titulos
        interes_bruto = inversion_cetes*(tasa / 364)*plazo
        isr = interes_bruto*0.015
        utilidad_neta = interes_bruto - isr
        capital_total = utilidad_neta+remanente+capital
        interes_neto_total = interes_neto_total + utilidad_neta

    capital_total = "${:,.2f}".format(capital_total)
    utilidad_neta = "${:,.2f}".format(utilidad_neta)
    data = [['Capital Inicial', "${:,.2f}".format(float(capital))], ['Plazo', f"{plazo} días"], ['Periodos', periodos], [
        'Interes Neto', "${:,.2f}".format(float(interes_neto_total))], ['Capital Final', capital_total]]

    df = pd.DataFrame(data, columns=['Concepto', 'Valor'])
    return df
