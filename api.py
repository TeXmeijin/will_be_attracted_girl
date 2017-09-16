# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import main

app = Flask(__name__)

# @app.route('/getUser/<string:userId>', methods=['GET'])
# def get_user(userId):
@app.route('/result', methods=['POST'])
def result():
    user_input = request.get_json()['input']
    print(user_input)
    user_love_file_names = main.exec(user_input)

    # print(request)
    # user_love_file_names = ''

    result = {
        "result": user_love_file_names or '',
        }

    return make_response(jsonify(result))
    
@app.route('/index', methods=['GET'])
def index():
# index.html をレンダリングする
    counts = [i for i in range(10, 60)]
    for count in counts:
        counts[count - 10] = count + ( count % 5 * 100 )
    return render_template('index.html', counts=counts)
                           # message=message, title=title)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
