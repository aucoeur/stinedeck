from flask import Flask, render_template, request, redirect, url_for, Markup
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from datetime import datetime
from random import choice, shuffle
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/stinedeck?authSource=admin&retryWrites=false&w=majority')
client = MongoClient(f'{host}')
db = client.stinedeck

decks = db.decks
cards = db.cards

last_updated = decks.create_index([('date_lastupdated', ASCENDING)])

@app.context_processor
def recently_update():
    recent = decks.find(
        sort=[('date_lastupdated', -1)],
        limit=5)
    return dict(recent=recent)

@app.route('/')
def index():
    '''Show Index page'''
    body = Markup("Dear Diary, it's me Laganja. Today all the girls sat separate from me and I lived alone under a table.<br><br><center><img src='https://media.giphy.com/media/NudlVy6NXsXVm/source.gif'></center>")

    return render_template('index.html', body=body)

@app.route('/decks')
def show_all_decks():
    '''View all decks'''
    return render_template('decks.html', decks=decks.find())

@app.route('/deck/create')
def create_deck():
    '''Show Create New Deck page'''
    title = "Create a New Deck"
    return render_template('create_new.html', deck={}, title=title)

@app.route('/deck', methods=['POST'])
def submit_deck():
    timestamp = datetime.utcnow()
    deck = {
        'date_created': timestamp,
        'date_lastupdated': timestamp,
        'title': request.form.get('title'),
        'tags': request.form.get('tags').split(" ")
    }
    deck_id = decks.insert_one(deck).inserted_id
    return redirect(url_for('show_deck', deck_id=deck_id))

@app.route('/deck/<deck_id>')
def show_deck(deck_id):
    '''Show single Deck'''
    action = "Add"
    deck = decks.find_one({'_id': ObjectId(deck_id)})
    card_deck = cards.find({'deck_id': ObjectId(deck_id)})
    return render_template('deck.html', action=action, deck=deck, card_deck=card_deck)

@app.route('/deck/<deck_id>/edit')
def edit_deck(deck_id):
    '''Display Edit Deck form'''
    deck = decks.find_one({'_id': ObjectId(deck_id)})
    return render_template('edit_deck.html', deck=deck)

@app.route('/deck/<deck_id>', methods=['POST'])
def submit_deck_edit(deck_id):
    '''Submit Edit Deck form'''
    updated_deck = {
        'date_lastupdated': datetime.utcnow(),
        'title': request.form.get('title'),
        'tags': request.form.get('tags').split(" ")
    }
    decks.update_one(
        {'_id': ObjectId(deck_id)},
        {'$set': updated_deck})
    return redirect(url_for('show_deck', deck_id=deck_id))

@app.route('/deck/<deck_id>/delete', methods=['POST'])
def deck_delete(deck_id):
    '''Delete deck'''
    decks.delete_one({'_id': ObjectId(deck_id)})
    return redirect(url_for('show_all_decks'))

@app.route('/deck/add', methods=['POST'])
def submit_card():
    '''Submit New Card form'''
    card = {
        'front': request.form.get('front'),
        'back': request.form.get('back'),
        'deck_id': ObjectId(request.form.get('deck_id'))
    }

    cards.insert_one(card).inserted_id
    return redirect(url_for('show_deck', deck_id=request.form.get('deck_id')))

@app.route('/card/<card_id>/edit')
def show_card_edit(card_id):
    '''Show single card edit page'''
    action = "Edit"
    card = cards.find_one({'_id': ObjectId(card_id)})
    deck = card['deck_id']
    return render_template('edit_card.html',
        action=action, card=card, deck=deck)

@app.route('/card/<card_id>', methods=['POST'])
def submit_card_edit(card_id):
    '''Submit Edit Card form'''
    updated_card = {
        'front': request.form.get('front'),
        'back': request.form.get('back')
    }
    cards.update_one(
        {'_id': ObjectId(card_id)},
        {'$set': updated_card})

    card = cards.find_one({'_id': ObjectId(card_id)})
    deck_id = card['deck_id']
    return redirect(url_for('show_deck', deck_id=deck_id))

@app.route('/card/<card_id>/delete', methods=['POST'])
def card_delete(card_id):
    '''Delete card'''
    card = cards.find_one({'_id': ObjectId(card_id)})
    deck_id = card['deck_id']
    cards.delete_one({'_id': ObjectId(card_id)})
    return redirect(url_for('show_deck', deck_id=deck_id))

@app.route('/deck/<deck_id>/review')
def review_deck(deck_id):
    '''Show review deck page'''
    deck_cards = cards.find({'deck_id': ObjectId(deck_id)})
    deck = decks.find_one({'_id': ObjectId(deck_id)})
    return render_template('review.html', deck_cards=deck_cards, deck=deck)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
