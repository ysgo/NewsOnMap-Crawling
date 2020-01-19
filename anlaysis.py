from decouple import config
import urllib3
import json
from zone_info import connect_mysql


def data_analysis(analysis_data):
    open_api_url = "http://aiopen.etri.re.kr:8000/WiseNLU"
    access_key = config('ETRI.KEY')
    analysis_code = "ner"
    titles = analysis_data['title']
    contents = analysis_data['content']
    text_len = len(titles)
    for i in range(text_len):
        text = titles[i] + contents[i]
        request_json = {
            "access_key": access_key,
            "argument": {
                "text": text,
                "analysis_code": analysis_code
            }
        }
        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            open_api_url,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(request_json)
        )
        print("[responseCode] " + str(response.status))
        print("[responBody]")
        response = json.loads(response.data.decode('utf-8'))
        return_object = response['return_object']
        sentences = return_object['sentence']
        print(sentences)
        analysis = Analysis()
        for sentence in sentences:
            recognition_results = sentence['NE']
            print(recognition_results)
            for info in recognition_results:
                info_name = info['text']
                print(info_name)
                info_type = str(info['type'])
                print(info_type)
                name_len = len(info_name)
                print(name_len)
                loc_list = ['PROVINCE', 'CAPITALCITY', 'ISLAND', 'CITY', 'COUNTY']
                first_name = []
                if info_type.endswith(loc_list):
                    if name_len == 5:
                        info_name = info_name[:2]
                    elif name_len >= 4:
                        info_name = info_name[0] + info_name[2]
                    elif name_len >= 3:
                        info_name = info_name[:2]
                    else:
                        if name_len != 1:
                            first_name.append(info_name[:1])
                    print(info_name)
                    if name_len == 1:
                        for data in first_name:
                            analysis.name_first = data
                        analysis.name_second = info_name
                    else:
                        analysis.name_first = info_name[0:1]
                        analysis.name_second = info_name[1:2]
    return response


def insert_zone_check(analysis):
    connect = connect_mysql()
    cursor = connect.cursor()
    temp = 0
    sql = ''
    cursor.execute(sql, ())



class Analysis:
    name_first = None
    name_second = None
    provinces = set()
    sigungus = set()

    def get_total_count(self):
        return len(self.provinces) + len(self.sigungus)
