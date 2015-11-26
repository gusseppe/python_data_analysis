
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
import plotly.plotly as ply
from plotly.graph_objs import Figure, Layout, XAxis, YAxis
from flask import Flask, request, render_template, redirect, url_for
from forms import SymbolSearch
import os


ply.sign_in('gusseppe', 'c6rox15e9r')

def df_to_plotly(df):
    '''
    Convertir de pandas a plotly
    '''
    if df.index.__class__.__name__=="DatetimeIndex":
        x = df.index.format()
    else:
        x = df.index.values 
    lines = {}
    for key in df:
        lines[key] = {}
        lines[key]['x'] = x
        lines[key]['y'] = df[key].values
        lines[key]['name'] = key
    lines_plotly = [lines[key] for key in df]
    return lines_plotly


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    form = SymbolSearch(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('results', symbol=request.form['symbol'],
                            trend1=request.form['trend1'],
                            trend2=request.form['trend2']))
    return render_template('selection.html', form=form)

@app.route("/symbol/<symbol>+<trend1>+<trend2>")
def results(symbol, trend1, trend2):
    data = web.DataReader(symbol, data_source='yahoo')

    #Guardamos la data en formato HDF5
#    filename = 'data'+'_'+symbol+'_'+trend1+'_'+trend2+'.h5'
    filename = 'data.h5'
    store = {}

    store['symbol'] = data
    h5 = pd.HDFStore(filename, 'w')
    h5['symbol'] = store['symbol']
    h5.close()

    #Mandamos la data al correo
    #os.system("python send_email.py")

    data['Tendencia 1'] = pd.rolling_mean(data['Adj Close'], window=int(trend1))
    data['Tendencia 2'] = pd.rolling_mean(data['Adj Close'], window=int(trend2))
    layout = Layout(
        xaxis=XAxis(showgrid=True, gridcolor='#bdbdbd', gridwidth=2),
        yaxis=YAxis(showgrid=True, gridcolor='#bdbdbd', gridwidth=2)
    )
    fig = Figure(data=df_to_plotly(data[['Adj Close', 'Tendencia 1', 'Tendencia 2']]),
                layout=layout)
    plot = ply.plot(fig, auto_open=False)
    table = data.tail().to_html()
    return render_template('plotly.html', symbol=symbol,
                            plot=plot, table=table)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
