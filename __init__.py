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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)