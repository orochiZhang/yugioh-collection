# -*- coding: UTF-8 -*-

from flask import Flask, jsonify
from flask import request
from controller import CardController

app = Flask(__name__)
card = CardController()


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

@app.route('/buy', methods=['GET'])
def buy_card():
    id = int(request.args.get("id", 0))
    data = card.buy_card(id)
    return jsonify(data)

@app.route('/nocard', methods=['GET'])
def no_card():
    id = int(request.args.get("id", 0))
    data = card.no_card(id)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)