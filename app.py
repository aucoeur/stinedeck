from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/stinedeck')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
decks = db.decks

decks.drop()

decks.insert_many([
    {"English": "go", "Romaji": "ikimasu", "Hiragana": "いきます", "Kanji": "行きます"},
    {"English": "come", "Romaji": "kimasu", "Hiragana": "きます", "Kanji": "来ます"},
    {"English": "eat", "Romaji": "tabemasu", "Hiragana": "たべます", "Kanji":"食べます"},
    {"English": "drink", "Romaji": "nomimasu", "Hiragana": "のみます", "Kanji": "飲みます"},
    {"English": "speak", "Romaji": "hanashimasu", "Hiragana":"はなします", "Kanji": "話します"},
    {"English": "listen", "Romaji": "kikimasu", "Hiragana": "ききます", "Kanji": "聞きます"},
    {"English": "read", "Romaji": "yomimasu", "Hiragana": "よみます", "Kanji": "読みます"},
    {"English": "write", "Romaji": "kakimasu", "Hiragana": "かきます", "Kanji": "書きます"},
    {"English": "watch", "Romaji": "mimasu", "Hiragana": "みます", "Kanji": "見ます"},
    {"English": "sleep", "Romaji": "nemasu", "Hiragana": "ねます", "Kanji": "寝ます"},
    {"English": "study", "Romaji": "benkyoo shimasu", "Hiragana": "べんきょうします", "Kanji": "勉強します"},
    {"English": "to hang out/play", "Romaji": "asobimasu", "Hiragana": "あそびます", "Kanji": "遊びます"},
    {"English": "from ~", "Romaji": "~kara", "Hiragana": "~から", "Kanji": ""},
    {"English": "to ~", "Romaji": "~made", "Hiragana": "~まで", "Kanji": ""},
    {"English": "year (at college)", "Romaji": "nensei", "Hiragana": "ねんせい", "Kanji": "年生"},
    {"English": "bus", "Romaji": "basu", "Hiragana": "ばす", "Kanji": ""},
    {"English": "train", "Romaji": "densha", "Hiragana": "でんしゃ", "Kanji": ""},
    {"English": "home", "Romaji": "uchi", "Hiragana": "うち", "Kanji": ""}
    ])

@app.route('/')
def index():
    msg = "Dear Diary, it's me Laganja. Today all the girls sat separate from me and I lived alone under a table."
    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))