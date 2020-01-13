from flask import Flask
from crawling import startCrawling
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/news/crawling')
def index():
    get_news = startCrawling()
    if get_news is None:
        return 'empty', 200
    else:
        get_news.to_json(orient='index', force_ascii=False)
        return get_news.to_json(orient='index', force_ascii=False)


if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
