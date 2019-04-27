#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash import Dash
from flask import Flask

server = Flask('nssPCA')
app = Dash(server=server)

app.config.suppress_callback_exceptions = True
