from flask import Flask, render_template, request, redirect, url_for, Markup
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/stinedeck')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
decks = db.decks
cards = db.cards

decks.drop()
cards.drop()

@app.route('/')
def index():
    '''Show Index page'''
    title = "Home"
    body = Markup("Dear Diary, it's me Laganja. Today all the girls sat separate from me and I lived alone under a table.<br><br><center><img src='https://media.giphy.com/media/NudlVy6NXsXVm/source.gif'></center>")
    return render_template('index.html', body=body, title=title)

@app.route('/decks')
def show_all_decks():
    '''View all decks'''
    return render_template('decks.html', decks=decks.find())

@app.route('/deck/create')
def create_deck():
    '''Show Create New Deck page'''
    title = "Create a New Deck"
    return render_template('create_new.html', title=title)

@app.route('/deck', methods=['POST'])
def submit_deck():
    deck = {
        'title': request.form.get('title'),
        'tags': request.form.get('tags').split(" ")
    }
    deck_id = decks.insert_one(deck).inserted_id
    return redirect(url_for('show_deck', deck_id=deck_id))

@app.route('/deck/add', methods=['POST'])
def submit_card():
    '''Submit New Card form'''

    card = {
        'front': request.form.get('front'),
        'back': request.form.get('back'),
        'deck_id': ObjectId(request.form.get('deck_id'))
    }
    print(card)
    cards.insert_one(card).inserted_id
    return redirect(url_for('show_deck', deck_id=request.form.get('deck_id')))

@app.route('/deck/<deck_id>')
def show_deck(deck_id):
    '''Show single Deck'''
    deck = decks.find_one({'_id': ObjectId(deck_id)})
    card_deck = cards.find({'deck_id': ObjectId(deck_id)})
    return render_template('deck.html', deck=deck, card_deck=card_deck)

@app.route('/deck/<deck_id>/review')
def review_deck(deck_id):
    '''Show review deck page'''
    front = 'front'
    back = 'back'
    return render_template('review.html', front=front, back=back)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))