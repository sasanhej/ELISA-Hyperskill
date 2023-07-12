import pandas as pd
from scipy.optimize import curve_fit


def LR(x, A, B, C, D):
    return D + ((A - D)/(1+(x/C)**B))


def RLR(y, A, B, C, D):
    return C*(((A-D)/(y-D))-1)**(1/B)


def elisa_automation(raw, standard):
    elisa = pd.read_csv(raw)
    standard = pd.read_csv(standard)
    elisa['AverageOD'] = (elisa.OD1 + elisa.OD2) / 2
    elisa['CorrectedOD'] = elisa.AverageOD - elisa.loc[10, 'AverageOD']
    standard['AverageOD'] = (standard.OD1 + standard.OD2) / 2
    xdata = standard['Concentration (ng/ml)']
    ydata = standard.AverageOD
    popt, pcov = curve_fit(LR, xdata, ydata)
    parameters = (0.04222091, 0.73506411, 7.38040933, 1.05035043)
    A, B, C, D = popt
    elisa['Concentration (ng/ml)'] = RLR(elisa.CorrectedOD, A, B, C, D)
    LODvalue = 1 #(ng/ml)
    elisa['Protein detectable'] = elisa['Concentration (ng/ml)'] > LODvalue
    elisa.to_csv('elisa_result.csv')
    return elisa


files = [input(), input()]
#files = ['elisa_data.csv', 'standard_values.csv']
print(elisa_automation(files[0], files[1]))