import datetime as dt
import math

import numpy as np
import pandas as pd
import plotly.express as px

from cetes import Cetes


class resultado:
    def __init__(self, capital_total, interes, isr, periodos):
        self.capital_total = capital_total
        self.interes = interes
        self.isr = isr
        self.periodos = periodos


def calculo_cetes(capital_inicial, plazo, años):
    # TODO: Recortar plazo por N = 52 semanas (Por ejemplo)
    cetes = Cetes(str(int(plazo)))
    end_date = str(dt.date.today())
    tasas_2020 = cetes.get_data(date_end='2020-12-31', date_start='2020-01-01')
    tasas_2021 = cetes.get_data(date_end='2021-12-31', date_start='2021-01-01')
    tasas_2022 = cetes.get_data(date_end='2022-12-31', date_start='2022-01-01')
    tasas_2023 = cetes.get_data(date_end=end_date, date_start='2023-01-01')
    tasa_mean_2020 = np.mean(tasas_2020['value']/100)
    tasa_mean_2021 = np.mean(tasas_2021['value']/100)
    tasa_mean_2022 = np.mean(tasas_2022['value']/100)
    tasa_mean_2023 = np.mean(tasas_2023['value']/100)

    tasas = [tasa_mean_2020, tasa_mean_2021, tasa_mean_2022, tasa_mean_2023]
    periodos = int(años)*364/int(plazo)
    periodos = math.floor(periodos)
    capital_total = capital_inicial
    interes_neto_total = 0
    años_transurridos = 0
    capital_por_periodo = []

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
        precio = 10 / (1 + (tasa / 364) ** plazo)
        titulos = math.floor(capital/precio)
        remanente = capital % precio
        inversion_cetes = precio*titulos
        interes_bruto = inversion_cetes*(tasa / 364)*plazo
        isr = interes_bruto*0.015
        utilidad_neta = interes_bruto - isr
        capital_total = utilidad_neta+remanente+capital
        interes_neto_total = interes_neto_total + utilidad_neta

        capital_por_periodo.append({'Periodo': i+1, 'Capital': capital, 'Interes': interes_bruto,
                                    'ISR': isr, 'Capital Total': capital_total})

    capital_total = "${:,.2f}".format(capital_total)
    utilidad_neta = "${:,.2f}".format(utilidad_neta)
    data = [['Capital Inicial', "${:,.2f}".format(float(capital_inicial))], ['Plazo', f"{plazo} días"], ['Periodos', periodos], [
        'Interes Neto', "${:,.2f}".format(float(interes_neto_total))], ['Capital Final', capital_total]]

    capital_por_periodo = pd.DataFrame(capital_por_periodo)
    
    historico = px.line(capital_por_periodo, x="Periodo", y="Capital")
    
    historico.update_traces(line_color="#ff55a3")

    df = pd.DataFrame(data, columns=['Concepto', 'Valor'])

    return df, historico
