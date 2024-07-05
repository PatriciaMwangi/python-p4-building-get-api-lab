#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    return [bakery.to_dict() for bakery in Bakery.query.all()]

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter(Bakery.id==id).first()
    bake=bakery.to_dict()
    response=make_response(bake,200)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    prices=BakedGood.query.order_by(desc(BakedGood.price)).all()
    prices_list=[price.to_dict() for price in prices]
    
    response=make_response(prices_list,200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    prices=BakedGood.query.order_by(desc(BakedGood.price)).first()
    most_expensive=prices.to_dict()
    response=make_response(most_expensive,200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
