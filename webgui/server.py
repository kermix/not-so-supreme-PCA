#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash
from flask import Flask


class Context:
    def __init__(self):
        import pandas as pd

        self.raw_data = ""

        self.original_data = pd.DataFrame()
        self.data = self.original_data.copy()

        self.normalized_data = self.data.copy()

        self.covariance_matix = None

        self.transformed_data = self.normalized_data.copy()

        self.scaler = None
        self.PCA = None

        self.axis = 1

        self.calc_mean = False
        self.calc_std = False


server = Flask(__name__)
app = Dash(__name__, server=server)

app.config.suppress_callback_exceptions = True

app.context = Context()
