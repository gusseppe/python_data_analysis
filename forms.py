#
# Data input form
# forms.py
#

from wtforms import TextField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form

class SymbolSearch(Form):
    symbol = TextField('<b>Simbolo</b> (ejemplo:  GOOGL, FB, AAPL, MSFT)',
                        validators=[DataRequired()])
    trend1 = TextField('<b>Tendencia 1</b> (ejemplo 20, 42)', 
                        validators=[DataRequired()])
    trend2 = TextField('<b>Tendencia 2</b> (ejemplo 100, 252)',
                        validators=[DataRequired()])
    submit = SubmitField()
