from flask import Flask
from crawling import startCrawling
from flask_cors import CORS
from decouple import config

app = Flask(__name__)
CORS(app)


@app.route('/news/crawling')
def index():
    get_news = startCrawling()
    print(get_news)
    if get_news is None:
        return 'empty', 200
    else:
        get_news.to_json(orient='index', force_ascii=False)
        return get_news.to_json(orient='index', force_ascii=False)


if __name__ == '__main__':
    app.run(host=config('APP.URL'), port=int(config('APP.PORT')), debug=True)
