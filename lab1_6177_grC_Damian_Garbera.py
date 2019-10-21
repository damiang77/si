import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize

# Dane wejściowe dla programu
curr1 = 'GBP'
curr2 = 'EUR'
date_start = '2019-10-07'
date_end = '2019-10-18'

# Funkcja pobierająca dane z API NBP dla podanej waluty oraz zakresu dat
def get_currency(currency,start,end):
    res = urlopen('http://api.nbp.pl/api/exchangerates/rates/A/' + currency + '/'+ start +'/' + end +'/')
    json_data = res.read().decode('utf-8', 'replace')
    return json_data

# Pobranie danych z API na podstawie przygotowanych danych wejściowych
rate_gbp = get_currency(curr1, date_start, date_end)
rate_eur = get_currency(curr2, date_start, date_end)

# Funkcja zwarająca przygotowane dane do wykorzystania w wykresie - ustawienie indeksów na datę
def plot_data(obj):
    json_data = json.loads(obj)
    df = json_normalize(json_data['rates'])
    df['effectiveDate'] = pd.to_datetime(df['effectiveDate'])
    return df.set_index('effectiveDate')['mid']

# Utworzenie zmiennych z danymi do wykresów
plot_data1 = plot_data(rate_gbp)
plot_data2 = plot_data(rate_eur)

#Korelacja dwóch kursów
correlation = np.corrcoef (plot_data1, plot_data2)[0][1]

# # Rysowanie wykresu pokazującego wyliczoną korelację oraz wartość obydwu kursów w porównaniu do PLN.
plt.plot(plot_data1, 'ro', plot_data2,'go')
plt.title('Korelacja {} do {} = {}'.format(curr1, curr2, correlation))
plt.ylabel('kurs w PLN')
plt.xlabel('Data')
plt.legend([curr1, curr2])
plt.show()