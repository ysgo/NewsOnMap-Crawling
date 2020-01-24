from flask import Flask
from flask_cors import CORS
from decouple import config
from crawling import startCrawling
from zone_info import add_zone_info, exist_zone_info
from analysis import data_analysis

app = Flask(__name__)
CORS(app)


@app.route('/news/crawling')
def index():
    analysis_data = startCrawling()
    if analysis_data is None:
        return 'empty', 200
    else:
        result = data_analysis(analysis_data)
        return result
        # analysis_data.to_json(orient='index', force_ascii=False)
        # return analysis_data.to_json(orient='index', force_ascii=False)


@app.route('/news/zone/add')
def add_zone():
    result = add_zone_info()
    return 'Insert Success!' if result == 1 else result


@app.route('/news/zone/check')
def exist_zone():
    return exist_zone_info()


if __name__ == '__main__':
    app.run(host=config('APP.URL'), port=int(config('APP.PORT')), debug=True)
