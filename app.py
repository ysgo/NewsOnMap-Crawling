from flask import Flask
from flask_cors import CORS
from decouple import config
from crawling import startCrawling
from zone_info import add_zone_info

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


@app.route('/news/zone/add')
def add_zone():
    result = add_zone_info()
    return 'Insert Success!' if result == 1 else result


if __name__ == '__main__':
    app.run(host=config('APP.URL'), port=int(config('APP.PORT')), debug=True)
