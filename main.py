# -*- coding: UTF-8 -*-
from flask import Flask
from kernel import Kernel
from controller.card.route import card_app

import logging

logging.basicConfig(filename='./log/debug.log', encoding="utf8",
                    format='[%(asctime)s-%(levelname)s:%(message)s]', level=logging.DEBUG, filemode='a',
                    datefmt='%Y-%m-%d %I:%M:%S %p', )

app = Flask(__name__)
k = Kernel()

@app.after_request
def cors(environ):
    environ = k.after_request(environ)
    return environ
    
@app.before_request
def handle_middleware():
    k.before_request()

app.register_blueprint(card_app)

if __name__ == '__main__':
    app.run(debug=True)
