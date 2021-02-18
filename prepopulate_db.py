from pymongo import MongoClient
from datetime import datetime
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/stinedeck')
client = MongoClient(f'{host}?authSource=admin&retryWrites=false&w=majority')
db = client.stinedeck

decks = db.decks
cards = db.cards


deck_sampledoc = {
    "date_created": datetime.utcnow(),
    "date_lastupdated": datetime.utcnow(),
    "title": "Japanese 1 - Chapter 1 Vocab",
    "tags": ["japanese", "language", "vocabulary"]
}

deck_id = decks.insert_one(deck_sampledoc)
print(deck_id.inserted_id)

# {"English": "home", "Romaji": "uchi", "Hiragana": "うち", "Kanji": ""}

# data = [{"English": "go", "Romaji": "ikimasu", "Hiragana": "いきます", "Kanji": "行きます"},
#     {"English": "come", "Romaji": "kimasu", "Hiragana": "きます", "Kanji": "来ます"},
#     {"English": "eat", "Romaji": "tabemasu", "Hiragana": "たべます", "Kanji":"食べます"},
#     {"English": "drink", "Romaji": "nomimasu", "Hiragana": "のみます", "Kanji": "飲みます"},
#     {"English": "speak", "Romaji": "hanashimasu", "Hiragana":"はなします", "Kanji": "話します"},
#     {"English": "listen", "Romaji": "kikimasu", "Hiragana": "ききます", "Kanji": "聞きます"},
#     {"English": "read", "Romaji": "yomimasu", "Hiragana": "よみます", "Kanji": "読みます"},
#     {"English": "write", "Romaji": "kakimasu", "Hiragana": "かきます", "Kanji": "書きます"},
#     {"English": "watch", "Romaji": "mimasu", "Hiragana": "みます", "Kanji": "見ます"},
#     {"English": "sleep", "Romaji": "nemasu", "Hiragana": "ねます", "Kanji": "寝ます"},
#     {"English": "study", "Romaji": "benkyoo shimasu", "Hiragana": "べんきょうします", "Kanji": "勉強します"},
#     {"English": "to hang out/play", "Romaji": "asobimasu", "Hiragana": "あそびます", "Kanji": "遊びます"},
#     {"English": "from ~", "Romaji": "~kara", "Hiragana": "~から", "Kanji": ""},
#     {"English": "to ~", "Romaji": "~made", "Hiragana": "~まで", "Kanji": ""},
#     {"English": "year (at college)", "Romaji": "nensei", "Hiragana": "ねんせい", "Kanji": "年生"},
#     {"English": "bus", "Romaji": "basu", "Hiragana": "ばす", "Kanji": ""},
#     {"English": "train", "Romaji": "densha", "Hiragana": "でんしゃ", "Kanji": ""},
#     {"English": "home", "Romaji": "uchi", "Hiragana": "うち", "Kanji": ""}]
