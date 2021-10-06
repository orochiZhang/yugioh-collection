# -*- coding: UTF-8 -*-

from flask import Flask, jsonify
from flask import request
from controller import CardController

app = Flask(__name__)
card = CardController()

@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    return environ

@app.route('/', methods=['GET'])
def show_card():
    page = int(request.args.get("page", 0))
    isbuy = int(request.args.get("isbuy", 10))
    data = card.show_card(page, isbuy)
    return jsonify(data)

@app.route('/search', methods=['GET'])
def search_card():
    content = str(request.args.get("content", ""))
    isbuy = int(request.args.get("isbuy", 0))
    data = card.search_card(content, isbuy)
    return jsonify(data)

@app.route('/search/name', methods=['GET'])
def search_card_by_name():
    content = str(request.args.get("content", ""))
    isbuy = int(request.args.get("isbuy", 0))
    data = card.search_card_by_name(content, isbuy)
    return jsonify(data)

@app.route('/search/packnumber', methods=['GET'])
def search_card_by_pack_number():
    content = str(request.args.get("content", ""))
    isbuy = int(request.args.get("isbuy", 10))
    data = card.search_card_by_pack_number(content, isbuy)
    return jsonify(data)

@app.route('/buy', methods=['GET'])
def buy_card():
    id = int(request.args.get("id", 10))
    data = card.buy_card(id)
    return jsonify(data)

@app.route('/nocard', methods=['GET'])
def no_card():
    id = int(request.args.get("id", 10))
    data = card.no_card(id)
    return jsonify(data)

@app.route('/count', methods=['GET'])
def count():
    data = card.count()
    return jsonify(data)

@app.route('/pack_list', methods=['GET'])
def get_pack_list():
    data = card.get_pack_list()
    return jsonify(data)

@app.route('/pack_info', methods=['GET'])
def get_pack_info():
    series = request.args.get("series", "")
    pack = request.args.get("pack", "")
    data = card.get_pack_info(series, pack)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)