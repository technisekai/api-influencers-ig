from scrap_instagram import *
from connect_db import *
import warnings
from flask import jsonify, Flask, Response, request, redirect

warnings.filterwarnings('ignore')

app = Flask(__name__)

# get data
@app.route('/')
def get_data():
    query_get = 'SELECT * FROM basic_information_account'
    cursor.execute(query_get)
    data = cursor.fetchall()
    return jsonify(data)

# add or synchronize 1 account
@app.route('/update', methods=['POST'])
def update_data():
    if request.method == 'POST':
        username = request.args.get('username')
        update(username=username)
        return get_data()

# synchronize data
@app.route('/sync')
def sync_data():
    sync()
    return get_data()

if __name__ == '__main__':
    app.run(debug=True)