import app.crawler as crawler
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/crawler', methods=['POST'])
def postInput():
    requests = request.get_json()
    bombLimit = requests['bombLimit']
    dateBegin = requests['dateBegin']
    dateEnd = requests['dateEnd']
    dic = crawler.main(dateBegin, dateEnd, bombLimit)
    return dic