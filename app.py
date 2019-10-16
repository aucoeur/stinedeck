from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    msg = "Dear Diary, it's me Laganja. Today all the girls sat separate from me and I lived alone under a table."
    return render_template('index.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))